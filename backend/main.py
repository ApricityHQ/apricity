import asyncio
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
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END

from pdf_ingest import extract_pdf_text
from text_chunking import chunk_text
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
    chunks = chunk_text(content)
    if not chunks:
        raise ValueError("No content available to index")

    vector_store = Chroma.from_documents(chunks, embeddings)
    return vector_store.as_retriever(), len(chunks)


format_docs = RunnableLambda(lambda docs: "\n\n".join(doc.page_content for doc in docs))


# -------------------------------------------------------------------
# Agent Prompt Templates
# -------------------------------------------------------------------
def agent_prompt(role: str, focus: str):
    return ChatPromptTemplate.from_messages([
        ("system", f"""
You are a {role}.

Rules:
- Be concise and factual
- DO NOT use conversational phrases
- DO NOT say: "Certainly", "Here is", "Here's", "In conclusion"
- DO NOT add introductions or summaries
- Use short bullet points only
- Max 5 bullets per section
- No filler text

Analyze ONLY the following aspects:
{focus}

Context:
{{context}}
"""),
        ("human", "Provide your analysis.")
    ])




FINANCIAL_PROMPT = agent_prompt(
    "Financial Analyst",
    "- Revenue model\n- Cost structure\n- Financial viability\n- Forecasts\n- ROI potential"
)

VC_PROMPT = agent_prompt(
    "Venture Capitalist",
    "- Investment readiness\n- Scalability\n- Market traction\n- Risk factors\n- Exit potential"
)

CTO_PROMPT = agent_prompt(
    "Chief Technology Officer",
    "- Technical feasibility\n- Architecture\n- Innovation\n- Scalability\n- Technical risks"
)

MARKETING_PROMPT = agent_prompt(
    "Marketing Specialist",
    "- Target market\n- Go-to-market strategy\n- Brand positioning\n- Customer acquisition\n- Competitive landscape"
)

PRODUCT_PROMPT = agent_prompt(
    "Product Analyst",
    "- Product-market fit\n- User needs\n- Feature set\n- Differentiation\n- Adoption barriers"
)


# -------------------------------------------------------------------
# Retrieval Queries (Keyword-focused)
# -------------------------------------------------------------------
RETRIEVAL_QUERIES = {
    "financial": "revenue model cost structure financial viability forecasts ROI",
    "vc": "investment readiness scalability market traction risk factors exit potential",
    "cto": "technical feasibility architecture innovation scalability technical risks",
    "marketing": "target market go-to-market strategy brand positioning customer acquisition competitive landscape",
    "product": "product-market fit user needs feature set differentiation adoption barriers"
}


# -------------------------------------------------------------------
# Agent Nodes
# -------------------------------------------------------------------
async def financial_agent(state):
    retriever = state["retriever"]
    query = RETRIEVAL_QUERIES["financial"]
    chain = (
        {"context": retriever | format_docs}
        | FINANCIAL_PROMPT
        | analysis_llm
        | StrOutputParser()
    )
    return {"financial": await chain.ainvoke(query)}


async def vc_agent(state):
    retriever = state["retriever"]
    query = RETRIEVAL_QUERIES["vc"]
    chain = (
        {"context": retriever | format_docs}
        | VC_PROMPT
        | analysis_llm
        | StrOutputParser()
    )
    return {"vc": await chain.ainvoke(query)}


async def cto_agent(state):
    retriever = state["retriever"]
    query = RETRIEVAL_QUERIES["cto"]
    chain = (
        {"context": retriever | format_docs}
        | CTO_PROMPT
        | analysis_llm
        | StrOutputParser()
    )
    return {"cto": await chain.ainvoke(query)}


async def marketing_agent(state):
    retriever = state["retriever"]
    query = RETRIEVAL_QUERIES["marketing"]
    chain = (
        {"context": retriever | format_docs}
        | MARKETING_PROMPT
        | analysis_llm
        | StrOutputParser()
    )
    return {"marketing": await chain.ainvoke(query)}


async def product_agent(state):
    retriever = state["retriever"]
    query = RETRIEVAL_QUERIES["product"]
    chain = (
        {"context": retriever | format_docs}
        | PRODUCT_PROMPT
        | analysis_llm
        | StrOutputParser()
    )
    return {"product": await chain.ainvoke(query)}


# -------------------------------------------------------------------
# LangGraph Definition (Parallel Agents)
# -------------------------------------------------------------------
class GraphState(dict):
    retriever: Any
    financial: str
    vc: str
    cto: str
    marketing: str
    product: str


graph = StateGraph(GraphState)

graph.add_node("financial_agent", financial_agent)
graph.add_node("vc_agent", vc_agent)
graph.add_node("cto_agent", cto_agent)
graph.add_node("marketing_agent", marketing_agent)
graph.add_node("product_agent", product_agent)

# Parallel execution
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

    try:
        retriever, chunk_count = build_retriever(combined_text)
        logger.info("Retriever built: %d chunks", chunk_count)
    except Exception as exc:
        logger.exception("build_retriever failed")
        raise HTTPException(status_code=500, detail=f"Failed to build retriever: {exc}")

    analysis_task = app_graph.ainvoke({"retriever": retriever})
    competitors_task = company_search_service.find_top_competitors_for_idea(prompt)

    logger.info("Awaiting analysis_task and competitors_task in parallel...")
    (
        analysis_result,
        competitors_result,
    ) = await asyncio.gather(
        analysis_task,
        competitors_task,
        return_exceptions=True
    )

    if isinstance(analysis_result, Exception):
        logger.error(
            "LangGraph analysis failed:\n%s",
            "".join(traceback.format_exception(type(analysis_result), analysis_result, analysis_result.__traceback__))
        )
        raise HTTPException(status_code=500, detail=f"Analysis failed: {analysis_result}")

    if isinstance(competitors_result, Exception):
        logger.warning(
            "Competitor search failed (non-fatal):\n%s",
            "".join(traceback.format_exception(type(competitors_result), competitors_result, competitors_result.__traceback__))
        )

    logger.info("Analysis complete. Agent result keys: %s", list(analysis_result.keys()))

    response: Dict[str, Any] = {
        "financial_analysis": analysis_result.get("financial"),
        "vc_analysis": analysis_result.get("vc"),
        "cto_analysis": analysis_result.get("cto"),
        "marketing_analysis": analysis_result.get("marketing"),
        "product_analysis": analysis_result.get("product")
    }

    if isinstance(competitors_result, Exception):
        response.update({
            "competitor_search_status": "error",
            "idea_search_sentence": None,
            "competitors": [],
            "competitor_search_error": str(competitors_result)
        })
    else:
        response.update({
            "competitor_search_status": competitors_result.get("status"),
            "idea_search_sentence": competitors_result.get("search_sentence"),
            "competitors": competitors_result.get("competitors", []),
            "competitor_search_error": competitors_result.get("error")
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
