from pydantic import BaseModel
from typing import List


class PdfRecord(BaseModel):
    pdf_id: str
    original_filename: str
    stored_pdf_filename: str
    pdf_path: str
    text_path: str
    chars_extracted: int
    uploaded_at_utc: str


class PdfUploadResponse(BaseModel):
    message: str
    pdf_id: str
    chars_extracted: int
    preview_500_chars: str


class PdfGetResponse(BaseModel):
    record: PdfRecord
    preview_500_chars: str


class PdfListResponse(BaseModel):
    count: int
    items: List[PdfRecord]
