import asyncio
import argparse
import json
import logging
import os
import time
from typing import Any, Dict, List

import httpx
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


logger = logging.getLogger(__name__)


ENRICHMENT_FIELDS: List[str] = [
    "company_differentiator",
    "funding",
    "revenue",
    "employees",
    "founded_year",
    "target_customer",
    "headquarters",
]

IDEA_SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You convert a startup idea into one short search sentence.

Rules:
- Return exactly one sentence
- Keep it under 24 words
- Include product + target customer + problem
- Do not include quotes, labels, or numbering
"""
    ),
    ("human", "{idea}")
])

DEEP_SEARCH_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["companies"],
    "properties": {
        "companies": {
            "type": "array",
            "description": "List of competitor companies",
            "items": {
                "type": "object",
                "required": ["company_name", "description", "funding", "employees", "headquarters"],
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "Name of the company"
                    },
                    "description": {
                        "type": "string",
                        "description": "One-sentence description including differentiator, target customer, revenue estimate, and founded year"
                    },
                    "funding": {
                        "type": "string",
                        "description": "Total funding raised and latest funding stage"
                    },
                    "employees": {
                        "type": "string",
                        "description": "Approximate employee count"
                    },
                    "headquarters": {
                        "type": "string",
                        "description": "Headquarters city and country"
                    },
                },
            },
        }
    },
}


def _clamp_competitor_limit(value: int, default: int = 25) -> int:
    return max(1, min(50, value or default))


class CompanySearchService:
    def __init__(
        self,
        *,
        openai_api_key: str,
        exa_api_key: str | None,
        exa_base_url: str = "https://api.exa.ai",
        summarizer_model: str = "gpt-4o-mini",
        competitor_limit: int = 25
    ) -> None:
        self.exa_api_key = exa_api_key
        self.exa_base_url = exa_base_url
        self.competitor_limit = _clamp_competitor_limit(competitor_limit)
        self.summary_llm = ChatOpenAI(
            model=summarizer_model,
            api_key=openai_api_key,
            temperature=0
        )

    @classmethod
    def from_env(cls, openai_api_key: str) -> "CompanySearchService":
        raw_limit = os.getenv("EXA_COMPETITOR_LIMIT", "25")
        try:
            competitor_limit = int(raw_limit)
        except ValueError:
            competitor_limit = 25

        return cls(
            openai_api_key=openai_api_key,
            exa_api_key=os.getenv("EXA_API_KEY"),
            exa_base_url=os.getenv("EXA_BASE_URL", "https://api.exa.ai"),
            summarizer_model=os.getenv("OPENAI_SUMMARIZER_MODEL", "gpt-4o-mini"),
            competitor_limit=competitor_limit
        )

    async def summarize_idea_for_company_search(self, idea: str) -> str:
        logger.info("company_search.summarize.start chars=%s", len(idea or ""))
        chain = IDEA_SUMMARY_PROMPT | self.summary_llm | StrOutputParser()
        summary = (await chain.ainvoke({"idea": idea})).strip()
        summary = " ".join(summary.split())
        if summary and summary[-1] not in ".!?":
            summary += "."
        logger.info("company_search.summarize.done chars=%s", len(summary))
        return summary

    def _get_exa_headers(self) -> Dict[str, str]:
        if not self.exa_api_key:
            raise RuntimeError("EXA_API_KEY not set")
        return {
            "x-api-key": self.exa_api_key,
            "Content-Type": "application/json"
        }

    def _stringify(self, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return " ".join(value.split())
        if isinstance(value, list):
            return " | ".join(part for part in (self._stringify(v) for v in value) if part)
        if isinstance(value, dict):
            for key in ("text", "value", "answer", "summary", "output"):
                if key in value and value[key]:
                    return self._stringify(value[key])
            for key in ("result", "results"):
                if key in value and value[key]:
                    return self._stringify(value[key])
            return ""
        return str(value)

    def _normalize_url(self, url: str) -> str:
        normalized = (url or "").strip()
        if not normalized:
            return ""
        if normalized.startswith("http://") or normalized.startswith("https://"):
            return normalized
        return f"https://{normalized}"

    # ------------------------------------------------------------------
    # Entity data extraction helpers (from Exa company search entities)
    # ------------------------------------------------------------------

    def _extract_entity_fields(self, entity: Dict[str, Any]) -> Dict[str, str]:
        props = entity.get("properties") if isinstance(entity.get("properties"), dict) else {}
        financials = props.get("financials") if isinstance(props.get("financials"), dict) else {}
        workforce = props.get("workforce") if isinstance(props.get("workforce"), dict) else {}
        hq = props.get("headquarters") if isinstance(props.get("headquarters"), dict) else {}
        latest_round = financials.get("fundingLatestRound") if isinstance(financials.get("fundingLatestRound"), dict) else {}

        funding_total = financials.get("fundingTotal")
        funding_str = "Unknown"
        if funding_total is not None:
            round_name = latest_round.get("name", "")
            funding_str = f"${funding_total:,.0f}"
            if round_name:
                funding_str += f" ({round_name})"

        revenue = financials.get("revenueAnnual")
        revenue_str = f"${revenue:,.0f}" if revenue else "Unknown"

        employees_total = workforce.get("total")
        employees_str = str(employees_total) if employees_total else "Unknown"

        founded = props.get("foundedYear")
        founded_str = str(founded) if founded else "Unknown"

        hq_parts = [p for p in [hq.get("city"), hq.get("country")] if p]
        hq_str = ", ".join(hq_parts) or "Unknown"

        return {
            "company_name": self._stringify(props.get("name")) or "Unknown",
            "description": self._stringify(props.get("description")) or "Unknown",
            "company_differentiator": "Unknown",
            "funding": funding_str,
            "revenue": revenue_str,
            "employees": employees_str,
            "founded_year": founded_str,
            "target_customer": "Unknown",
            "headquarters": hq_str,
        }

    # ------------------------------------------------------------------
    # Exa Search API (company category) — replaces Websets
    # ------------------------------------------------------------------

    async def _search_companies(
        self, client: httpx.AsyncClient, search_sentence: str, limit: int
    ) -> List[Dict[str, Any]]:
        logger.info("company_search.search_api.start limit=%s", limit)
        capped = min(limit, 100)

        payload: Dict[str, Any] = {
            "query": f"Find direct competitors for this startup idea: {search_sentence}",
            "type": "auto",
            "category": "company",
            "numResults": capped,
            "contents": {
                "highlights": {"maxCharacters": 2000}
            },
        }

        response = await client.post(
            f"{self.exa_base_url}/search",
            json=payload,
            headers=self._get_exa_headers(),
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        logger.info("company_search.search_api.done count=%s", len(results))
        return results

    async def _deep_search_companies(
        self, client: httpx.AsyncClient, search_sentence: str, limit: int
    ) -> Dict[str, Any] | None:
        logger.info("company_search.deep_search.start limit=%s", limit)
        capped = min(limit, 100)

        payload: Dict[str, Any] = {
            "query": f"Find {capped} direct competitors for this startup idea: {search_sentence}",
            "type": "deep",
            "category": "company",
            "numResults": capped,
            "outputSchema": DEEP_SEARCH_OUTPUT_SCHEMA,
        }

        response = await client.post(
            f"{self.exa_base_url}/search",
            json=payload,
            headers=self._get_exa_headers(),
        )
        response.raise_for_status()
        data = response.json()

        output = data.get("output")
        if isinstance(output, dict):
            content = output.get("content")
            if isinstance(content, str):
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    pass
            elif isinstance(content, dict):
                return content

        logger.info("company_search.deep_search.done")
        return None

    # ------------------------------------------------------------------
    # Build competitor dicts from different response shapes
    # ------------------------------------------------------------------

    def _format_from_search_result(self, item: Dict[str, Any], rank: int) -> Dict[str, Any]:
        entities = item.get("entities", [])
        entity_fields: Dict[str, str] = {}
        if isinstance(entities, list):
            for e in entities:
                if isinstance(e, dict) and e.get("type") == "company":
                    entity_fields = self._extract_entity_fields(e)
                    break

        highlights = item.get("highlights", [])
        highlight_text = " ".join(highlights) if isinstance(highlights, list) else ""

        company_name = (
            entity_fields.get("company_name")
            or self._stringify(item.get("title"))
            or "Unknown"
        )
        description = (
            entity_fields.get("description")
            or highlight_text
            or self._stringify(item.get("summary"))
            or "Unknown"
        )
        website = self._normalize_url(self._stringify(item.get("url"))) or "Unknown"

        return {
            "rank": rank,
            "company_name": company_name,
            "website": website,
            "description": description,
            "company_differentiator": entity_fields.get("company_differentiator", "Unknown"),
            "funding": entity_fields.get("funding", "Unknown"),
            "revenue": entity_fields.get("revenue", "Unknown"),
            "employees": entity_fields.get("employees", "Unknown"),
            "founded_year": entity_fields.get("founded_year", "Unknown"),
            "target_customer": entity_fields.get("target_customer", "Unknown"),
            "headquarters": entity_fields.get("headquarters", "Unknown"),
        }

    def _format_from_deep_result(self, company: Dict[str, Any], rank: int) -> Dict[str, Any]:
        description = company.get("description", "Unknown")

        return {
            "rank": rank,
            "company_name": company.get("company_name", "Unknown"),
            "website": "Unknown",
            "description": description,
            "company_differentiator": "Unknown",
            "funding": company.get("funding", "Unknown"),
            "revenue": "Unknown",
            "employees": company.get("employees", "Unknown"),
            "founded_year": "Unknown",
            "target_customer": "Unknown",
            "headquarters": company.get("headquarters", "Unknown"),
        }

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    async def find_top_competitors_for_idea(self, idea: str, limit: int | None = None) -> Dict[str, Any]:
        safe_limit = _clamp_competitor_limit(limit or self.competitor_limit)
        start_time = time.monotonic()
        logger.info("company_search.run.start limit=%s exa_enabled=%s", safe_limit, bool(self.exa_api_key))
        search_sentence = await self.summarize_idea_for_company_search(idea)

        if not self.exa_api_key:
            logger.warning("company_search.run.disabled reason=missing_exa_api_key")
            return {
                "status": "disabled",
                "search_sentence": search_sentence,
                "competitors": [],
                "error": "EXA_API_KEY not configured"
            }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                # Primary: company search with entity data
                results = await self._search_companies(client, search_sentence, safe_limit)

                competitors = [
                    self._format_from_search_result(item, index + 1)
                    for index, item in enumerate(results)
                    if isinstance(item, dict)
                ]

                # Fallback: if auto search returned few results, try deep search
                if len(competitors) < max(3, safe_limit // 2):
                    logger.info("company_search.fallback_to_deep count=%s", len(competitors))
                    deep_result = await self._deep_search_companies(client, search_sentence, safe_limit)
                    if deep_result and isinstance(deep_result.get("companies"), list):
                        deep_companies = deep_result["companies"]
                        existing_names = {c["company_name"].lower() for c in competitors}
                        rank = len(competitors) + 1
                        for dc in deep_companies:
                            if isinstance(dc, dict) and dc.get("company_name", "").lower() not in existing_names:
                                competitors.append(self._format_from_deep_result(dc, rank))
                                existing_names.add(dc["company_name"].lower())
                                rank += 1
                                if len(competitors) >= safe_limit:
                                    break

                competitors = competitors[:safe_limit]

        except Exception:
            logger.exception("company_search.run.failed")
            raise

        elapsed = round(time.monotonic() - start_time, 3)
        logger.info(
            "company_search.run.done competitors=%s elapsed_seconds=%s",
            len(competitors),
            elapsed
        )
        return {
            "status": "completed",
            "search_sentence": search_sentence,
            "competitors": competitors
        }


def _configure_logging(level_name: str) -> None:
    level = getattr(logging, level_name.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="company_search",
        description="Run competitor discovery for a startup idea."
    )
    parser.add_argument("idea", help="Startup idea text to analyze.")
    parser.add_argument("--limit", type=int, default=None, help="Override competitor result limit.")
    parser.add_argument("--log-level", default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR).")
    return parser


def cli_main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    _configure_logging(args.log_level)
    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        logger.error("OPENAI_API_KEY is required to run company_search CLI")
        return 1

    service = CompanySearchService.from_env(openai_api_key)
    try:
        result = asyncio.run(service.find_top_competitors_for_idea(args.idea, limit=args.limit))
    except Exception:
        logger.exception("company_search.cli.failed")
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(cli_main())
