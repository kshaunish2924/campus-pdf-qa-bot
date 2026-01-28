from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extracts text from a PDF using pypdf.
    Returns a single combined string.
    """
    reader = PdfReader(str(pdf_path))

    texts = []
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        # Keep pages separated (helps later for chunking)
        texts.append(f"\n\n--- Page {i+1} ---\n{page_text}")

    return "".join(texts).strip()
