from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from .rag_pipeline import ask

app = FastAPI(
    title="Enterprise RAG API",
    version="1.0.0"
)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str


@app.get("/")
def root():
    return {
        "message": "Enterprise RAG API running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY not configured"
        )

    try:

        result = ask(
            question=request.question,
            api_key=api_key
        )

        return QueryResponse(
            answer=result["answer"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )