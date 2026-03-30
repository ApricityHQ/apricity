import logging
import os
import traceback
from contextlib import asynccontextmanager
from typing import Any, Dict

# ---- Load env FIRST — before any module that reads os.getenv at import time ----
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import aiosqlite

from company_search import CompanySearchService
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

from pdf_ingest import extract_pdf_text
from text_chunking import chunk_text, should_chunk
from agents import financial_agent, vc_agent, cto_agent, marketing_agent, product_agent
from db import init_db, get_db, save_report, get_user_reports, get_report_by_id, save_message, get_report_messages
from auth import get_current_user_id

# ---- Logging Setup ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("ssp.main")

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="Startup Success Predictor - Multi Agent", lifespan=lifespan)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")

ANALYSIS_MODEL = os.getenv("OPENAI_ANALYSIS_MODEL", "gpt-4o")

analysis_llm = ChatOpenAI(
    model=ANALYSIS_MODEL,
    api_key=OPENAI_API_KEY,
    temperature=0.3
)

embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
company_search_service = CompanySearchService.from_env(OPENAI_API_KEY)
# social_signals_service = SocialSignalsService.from_env()

# -------------------------------------------------------------------
# Shared RAG Utilities
# -------------------------------------------------------------------
def build_retriever(content: str):
    """
    Chunk the given content and index it into an in-memory Chroma vector store.

    Only called when the combined input text exceeds the RAG threshold (long inputs
    such as uploaded PDFs). For short inputs, context is passed directly to agents.

    Args:
        content: The full combined text to chunk and index.

    Returns:
        A tuple of (retriever, chunk_count) where retriever is a LangChain
        VectorStoreRetriever and chunk_count is the number of indexed chunks.

    Raises:
        ValueError: If content is empty or produces no chunks.
    """
    chunks = chunk_text(content)
    if not chunks:
        raise ValueError("No content available to index")

    vector_store = Chroma.from_documents(chunks, embeddings)
    return vector_store.as_retriever(), len(chunks)



# Agent prompts are defined in agents.py and imported above.

AGGREGATOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Senior Startup Evaluator synthesizing analyses from multiple experts.

Rules:
- Be concise and factual
- DO NOT use conversational phrases
- DO NOT say: "Certainly", "Here is", "Here's", "In conclusion"
- No filler text

You will receive analyses from 5 experts (Financial, VC, CTO, Marketing, Product) and a competitor landscape.

Produce EXACTLY this output format:

## Overall Assessment
<3-5 bullet points synthesizing the key findings across all perspectives>

## Key Strengths
<2-3 bullet points>

## Critical Risks
<2-3 bullet points>

## Success Probability: <Low|Medium|High>
<1 sentence justification>
"""),
    ("human", """STARTUP PITCH:
{pitch}

Expert Analyses:

FINANCIAL ANALYSIS:
{financial}

VC ANALYSIS:
{vc}

CTO ANALYSIS:
{cto}

MARKETING ANALYSIS:
{marketing}

PRODUCT ANALYSIS:
{product}

COMPETITOR LANDSCAPE:
{competitors}

Provide your overall evaluation.""")
])


# Retrieval queries and agent node functions are defined in agents.py and imported above.
# Agent nodes are wrapped below to close over the shared analysis_llm instance.


# -------------------------------------------------------------------
# LangGraph Definition (Parallel Agents)
# -------------------------------------------------------------------
class GraphState(dict):
    """
    Shared state passed through the LangGraph agent pipeline.

    Fields:
        pitch: Original startup description typed by the user.
        context: Full combined text used when RAG is skipped (short inputs).
        retriever: Chroma retriever instance when RAG is active (long inputs), else None.
        competitors: Pre-formatted competitor summary string fed to all agents.
        financial: Output from the financial analysis agent.
        vc: Output from the VC analysis agent.
        cto: Output from the CTO analysis agent.
        marketing: Output from the marketing analysis agent.
        product: Output from the product analysis agent.
    """
    pitch: str
    context: str
    retriever: Any
    competitors: str
    financial: str
    vc: str
    cto: str
    marketing: str
    product: str


# Wrap each agent to close over the shared LLM instance.
# This keeps agents.py stateless and testable without the LLM as a global.
async def _financial_node(state): return await financial_agent(state, analysis_llm)
async def _vc_node(state): return await vc_agent(state, analysis_llm)
async def _cto_node(state): return await cto_agent(state, analysis_llm)
async def _marketing_node(state): return await marketing_agent(state, analysis_llm)
async def _product_node(state): return await product_agent(state, analysis_llm)


graph = StateGraph(GraphState)

graph.add_node("financial_agent", _financial_node)
graph.add_node("vc_agent", _vc_node)
graph.add_node("cto_agent", _cto_node)
graph.add_node("marketing_agent", _marketing_node)
graph.add_node("product_agent", _product_node)

# financial_agent is the entry point; all others fan out from it in parallel.
graph.set_entry_point("financial_agent")

graph.add_edge("financial_agent", "vc_agent")
graph.add_edge("financial_agent", "cto_agent")
graph.add_edge("financial_agent", "marketing_agent")
graph.add_edge("financial_agent", "product_agent")

graph.add_edge("financial_agent", END)
graph.add_edge("vc_agent", END)
graph.add_edge("cto_agent", END)
graph.add_edge("marketing_agent", END)
graph.add_edge("product_agent", END)

app_graph = graph.compile()


# -------------------------------------------------------------------
# API Endpoint
# -------------------------------------------------------------------
@app.post("/view")
async def view_analysis(
    prompt: str = Form(...),
    files: list[UploadFile] | None = File(None),
    user_id: str | None = Depends(get_current_user_id),
    db: aiosqlite.Connection = Depends(get_db)
):
    logger.info("POST /view | user_id=%s | prompt_len=%d", user_id, len(prompt))
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    extracted_texts: list[str] = []
    if files:
        for upload in files:
            try:
                file_bytes = await upload.read()
                extracted_texts.append(extract_pdf_text(file_bytes))
            except Exception as exc:
                logger.exception("PDF extraction failed for %s", upload.filename)
                raise HTTPException(
                    status_code=400,
                    detail=f"PDF extraction failed for {upload.filename}: {exc}"
                )

    combined_text = "\n\n".join([text for text in [prompt, *extracted_texts] if text])

    # --- Step 1: Competitor search runs first so agents can reason about the market ---
    competitors_result = None
    try:
        competitors_result = await company_search_service.find_top_competitors_for_idea(prompt)
        logger.info("Competitor search complete: status=%s", competitors_result.get("status"))
    except Exception as exc:
        logger.warning(
            "Competitor search failed (non-fatal):\n%s",
            "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        )

    competitors_summary = "No competitor data available."
    if competitors_result and not isinstance(competitors_result, Exception):
        comps = competitors_result.get("competitors", [])
        if comps:
            competitors_summary = "\n".join(
                f"- {c.get('company_name', 'Unknown')}: {c.get('description', '')}"
                for c in comps
            )

    # --- Step 2: Build context — skip RAG for short inputs to avoid fragmentation ---
    if should_chunk(combined_text):
        try:
            retriever, chunk_count = build_retriever(combined_text)
            logger.info("Retriever built: %d chunks (RAG active)", chunk_count)
        except Exception as exc:
            logger.exception("build_retriever failed")
            raise HTTPException(status_code=500, detail=f"Failed to build retriever: {exc}")
        context = ""
    else:
        retriever = None
        context = combined_text
        logger.info("Short input (%d chars): passing full text directly, RAG skipped", len(combined_text))

    # --- Step 3: Run all 5 agents in parallel via LangGraph ---
    try:
        analysis_result = await app_graph.ainvoke({
            "pitch": prompt,
            "context": context,
            "retriever": retriever,
            "competitors": competitors_summary,
        })
    except Exception as exc:
        logger.error(
            "LangGraph analysis failed:\n%s",
            "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        )
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}")

    logger.info("Analysis complete. Agent result keys: %s", list(analysis_result.keys()))

    # --- Step 4: Aggregator synthesizes all agent outputs ---
    aggregator_chain = AGGREGATOR_PROMPT | analysis_llm | StrOutputParser()
    overall_evaluation = await aggregator_chain.ainvoke({
        "pitch": prompt,
        "financial": analysis_result.get("financial", ""),
        "vc": analysis_result.get("vc", ""),
        "cto": analysis_result.get("cto", ""),
        "marketing": analysis_result.get("marketing", ""),
        "product": analysis_result.get("product", ""),
        "competitors": competitors_summary,
    })

    response: Dict[str, Any] = {
        "overall_evaluation": overall_evaluation,
        "financial_analysis": analysis_result.get("financial"),
        "vc_analysis": analysis_result.get("vc"),
        "cto_analysis": analysis_result.get("cto"),
        "marketing_analysis": analysis_result.get("marketing"),
        "product_analysis": analysis_result.get("product")
    }

    if competitors_result:
        response.update({
            "competitor_search_status": competitors_result.get("status"),
            "idea_search_sentence": competitors_result.get("search_sentence"),
            "competitors": competitors_result.get("competitors", []),
            "competitor_search_error": competitors_result.get("error"),
        })
    else:
        response.update({
            "competitor_search_status": "error",
            "idea_search_sentence": None,
            "competitors": [],
            "competitor_search_error": "Competitor search failed or was unavailable.",
        })

    if user_id:
        try:
            report_id = await save_report(db, user_id, prompt, response)
            response["report_id"] = report_id
            logger.info("Report saved: %s", report_id)
        except Exception:
            logger.exception("Failed to save report to DB")

    return response

@app.get("/reports")
async def list_reports(
    user_id: str | None = Depends(get_current_user_id),
    db: aiosqlite.Connection = Depends(get_db)
):
    logger.info("GET /reports | user_id=%s", user_id)
    if not user_id:
        logger.warning("GET /reports rejected: no user_id (unauthenticated)")
        raise HTTPException(status_code=401, detail="Authentication required")
    try:
        reports = await get_user_reports(db, user_id)
        logger.info("GET /reports OK: %d reports", len(reports))
        return {"reports": reports}
    except Exception:
        logger.exception("GET /reports DB error")
        raise

@app.get("/reports/{report_id}")
async def get_report(
    report_id: str,
    user_id: str | None = Depends(get_current_user_id),
    db: aiosqlite.Connection = Depends(get_db)
):
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    report = await get_report_by_id(db, user_id, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@app.post("/chat/{report_id}")
async def chat_with_report(
    report_id: str,
    request: ChatRequest,
    user_id: str | None = Depends(get_current_user_id),
    db: aiosqlite.Connection = Depends(get_db)
):
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    report = await get_report_by_id(db, user_id, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    if not request.messages:
        raise HTTPException(status_code=400, detail="No messages provided")
        
    user_message = request.messages[-1].content
    await save_message(db, report_id, "user", user_message)

    async def generate():
        import json
        full_response = ""
        # Build prompt context
        report_context = json.dumps(report.get("result", {}))
        
        # We also pass the prior messages to retain memory in the LLM
        llm_messages = [
            ("system", "You are an AI assistant helping a startup founder refine and understand their generated report. Use Markdown. Be concise. Here is the full report context:\\n" + report_context)
        ]
        
        for msg in request.messages[:-1]:
            llm_messages.append((msg.role, msg.content))
            
        llm_messages.append(("human", user_message))
        
        try:
            async for chunk in analysis_llm.astream(llm_messages):
                if chunk.content:
                    full_response += chunk.content
                    # Vercel Data Stream Protocol Format: 0:"json encoded text"\n
                    yield f'0:{json.dumps(chunk.content)}\n'
                    
            # Save the final compiled response to DB
            await save_message(db, report_id, "assistant", full_response)
        except Exception as e:
            # Emit error stream format if needed: 3:"error message"\n
            yield f'3:{json.dumps(str(e))}\n'

    return StreamingResponse(generate(), media_type="text/plain")

@app.get("/chat/{report_id}")
async def get_chat_history(
    report_id: str,
    user_id: str | None = Depends(get_current_user_id),
    db: aiosqlite.Connection = Depends(get_db)
):
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
        
    report = await get_report_by_id(db, user_id, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    messages = await get_report_messages(db, report_id)
    return {"messages": messages}



# -------------------------------------------------------------------
# Run Server
# -------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
