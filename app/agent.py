import uuid
from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.rag import get_retriever
from app.prompts import SYSTEM_PROMPT, INTENT_PROMPT


# Structured output schema to guarantee intent classification values
class IntentResponse(BaseModel):
    intent: Literal["normal", "out_of_scope", "attack"] = Field(
        description="The classified target intent of the user's input query."
    )


# =========================
# Ticket Store (In-Memory Database Simulation)
# =========================
tickets = []


def create_support_ticket(user_message: str, reason: str) -> dict:
    """Creates a tracking support ticket when document context is unavailable."""
    ticket = {
        "ticket_id": f"DWL-{str(uuid.uuid4())[:8].upper()}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "open",
        "issue": user_message,
        "reason": reason
    }
    tickets.append(ticket)
    return ticket


# =========================
# LLM-BASED INTENT ROUTER
# =========================
intent_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_router = intent_llm.with_structured_output(IntentResponse)


def classify_intent(question: str) -> str:
    """Evaluates input strings for malicious behavior or scope alignment."""
    prompt = ChatPromptTemplate.from_template(INTENT_PROMPT)
    chain = prompt | structured_router
    
    try:
        result = chain.invoke({"query": question})
        return result.intent
    except Exception:
        # Graceful fallback to safety layer if LLM fails or hits validation schema exceptions
        return "attack"


# =========================
# Docs Formatting
# =========================
def format_docs(docs) -> str:
    if not docs:
        return ""
    return "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
        for doc in docs
    )


# =========================
# MAIN ENTRY POINT
# =========================
async def get_answer(question: str) -> dict:
    """
    Main RAG pipeline coordinating intent verification, 
    context loading, and dynamic response generation.
    """
    # 1. Intent Routing Layer
    intent = classify_intent(question)

    if intent == "attack":
        return {
            "question": question,
            "answer": "I can't help with that request.",
            "sources": [],
            "ticket": None,
            "intent": intent
        }

    if intent == "out_of_scope":
        return {
            "question": question,
            "answer": "That's outside the scope of what I can help with. I'm here to assist with Dwelleo platform-related questions.",
            "sources": [],
            "ticket": None,
            "intent": intent
        }

    # 2. Context Retrieval
    retriever = get_retriever()
    docs = retriever.invoke(question)
    context = format_docs(docs)

    # 3. Pre-LLM Deterministic Context Fallback
    if not docs or not context.strip():
        ticket = create_support_ticket(
            user_message=question,
            reason="No relevant match found in knowledge base"
        )
        return {
            "question": question,
            "answer": "I don't have enough information to answer that right now. Would you like me to create a support ticket for you?",
            "sources": [],
            "ticket": ticket,
            "intent": intent
        }

    # 4. LLM Generation Layer (Fixed Syntax Placement)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

    chain = (
        {
            "context": lambda x: context,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    raw_answer = await chain.ainvoke(question)

    # 5. Post-LLM Guardrail Check (Catches insufficient/roadmap vector leak answers)
    if "i do not have enough information" in raw_answer.lower():
        ticket = create_support_ticket(
            user_message=question, 
            reason="Retrieved documentation context was insufficient to fulfill the specific query."
        )
        return {
            "question": question,
            "answer": "I don't have enough information to answer that right now. Would you like me to create a support ticket for you?",
            "sources": [],
            "ticket": ticket,
            "intent": intent
        }

    return {
        "question": question,
        "answer": raw_answer.strip(),
        "sources": list(set(doc.metadata.get("source", "unknown") for doc in docs)),
        "ticket": None,
        "intent": intent
    }