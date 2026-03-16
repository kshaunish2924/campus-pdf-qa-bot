from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    pdf_id: str  # ← THIS WAS MISSING

class QueryResponse(BaseModel):
    answer: str