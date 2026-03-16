from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
from datetime import datetime, timezone

from backend.app.core.config import UPLOAD_DIR, TEXT_DIR, METADATA_PATH
from backend.app.services.pdf_extractor import extract_text_from_pdf
from backend.app.services.pdf_store import (
    upsert_pdf_record,
    get_pdf_record,
    list_pdf_records,
)

from backend.app.services.qa_service import prepare_document, answer_question
from backend.app.schemas.pdf import (
    PdfUploadResponse,
    PdfGetResponse,
    PdfListResponse,
    PdfRecord,
)

from backend.app.schemas.query import QueryRequest, QueryResponse

app = FastAPI(title="Campus PDF Q&A Bot")

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/ui")
def ui():
    return FileResponse("frontend/index.html")


# -------------------------------
# Health Check
# -------------------------------
@app.get("/")
def health():
    return {"status": "ok", "service": "campus-pdf-qa-bot"}


# -------------------------------
# Upload PDF
# -------------------------------
@app.post("/pdf/upload", response_model=PdfUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    pdf_id = uuid.uuid4().hex

    # Save PDF
    safe_pdf_name = f"{pdf_id}_{Path(file.filename).name}"
    pdf_path = UPLOAD_DIR / safe_pdf_name

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    pdf_path.write_bytes(contents)

    # Extract text
    extracted_text = extract_text_from_pdf(pdf_path)

    # Save extracted text
    text_path = TEXT_DIR / f"{pdf_id}.txt"
    text_path.write_text(extracted_text, encoding="utf-8")

    # Build vector index for this document
    prepare_document(pdf_id, extracted_text)

    # Save metadata
    record = {
        "pdf_id": pdf_id,
        "original_filename": file.filename,
        "stored_pdf_filename": safe_pdf_name,
        "pdf_path": str(pdf_path),
        "text_path": str(text_path),
        "chars_extracted": len(extracted_text),
        "uploaded_at_utc": datetime.now(timezone.utc).isoformat(),
    }

    upsert_pdf_record(METADATA_PATH, pdf_id, record)

    return {
        "message": "PDF uploaded, text extracted, and indexed.",
        "pdf_id": pdf_id,
        "chars_extracted": len(extracted_text),
        "preview_500_chars": extracted_text[:500],
    }


# -------------------------------
# Get PDF by ID
# -------------------------------
@app.get("/pdf/{pdf_id}", response_model=PdfGetResponse)
def get_pdf(pdf_id: str):

    record = get_pdf_record(METADATA_PATH, pdf_id)

    if not record:
        raise HTTPException(status_code=404, detail="pdf_id not found.")

    text_path = Path(record["text_path"])

    preview = ""
    if text_path.exists():
        preview = text_path.read_text(encoding="utf-8")[:500]

    return {
        "record": record,
        "preview_500_chars": preview,
    }


# -------------------------------
# List all PDFs
# -------------------------------
@app.get("/pdfs", response_model=PdfListResponse)
def list_pdfs():

    data = list_pdf_records(METADATA_PATH)

    items = [PdfRecord(**rec) for rec in data.values()]

    items.sort(key=lambda x: x.uploaded_at_utc, reverse=True)

    return {
        "count": len(items),
        "items": items,
    }


# -------------------------------
# Ask Question about PDF
# -------------------------------
@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):

    record = get_pdf_record(METADATA_PATH, request.pdf_id)

    if not record:
        raise HTTPException(status_code=404, detail="pdf_id not found.")

    answer = answer_question(request.pdf_id, request.question)

    return {
        "answer": answer
    }