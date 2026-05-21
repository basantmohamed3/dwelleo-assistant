from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import get_answer, tickets

app = FastAPI(
    title="Dwelleo Support Assistant",
    description="AI-powered support assistant for Dwelleo platform",
    version="1.0.0"
)

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask(request: QuestionRequest):
    # Fixed: Added 'await' to resolve the asynchronous coroutine object into a dictionary
    result = await get_answer(request.question)
    return result

@app.get("/tickets")
def get_tickets():
    return {"tickets": tickets}

@app.get("/health")
def health():
    return {"status": "ok"}