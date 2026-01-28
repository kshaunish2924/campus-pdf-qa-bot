from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import uuid

from backend.app.core.config import UPLOAD_DIR
from backend.app.services.pdf_extractor import extract_text_from_pdf

app = FastAPI(title="Campus PDF Q&A Bot")


@app.get("/")
def health():
    return {"status": "ok", "service": "campus-pdf-qa-bot"}


@app.post("/pdf/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # 1) Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # 2) Save uploaded PDF to backend/app/data/uploads
    safe_name = f"{uuid.uuid4().hex}_{Path(file.filename).name}"
    save_path = UPLOAD_DIR / safe_name

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    save_path.write_bytes(contents)

    # 3) Extract text
    extracted_text = extract_text_from_pdf(save_path)

    # 4) Temporary response (preview only)
    return {
        "message": "PDF uploaded and text extracted.",
        "original_filename": file.filename,
        "stored_filename": safe_name,
        "stored_path": str(save_path),
        "chars_extracted": len(extracted_text),
        "preview_500_chars": extracted_text[:500],
    }
