import json
from pathlib import Path
from typing import Dict, Any, Optional


def read_metadata(metadata_path: Path) -> Dict[str, Any]:
    if not metadata_path.exists():
        return {}

    raw = metadata_path.read_text(encoding="utf-8").strip()
    if not raw:
        return {}

    return json.loads(raw)


def write_metadata(metadata_path: Path, data: Dict[str, Any]) -> None:
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def get_pdf_record(metadata_path: Path, pdf_id: str) -> Optional[Dict[str, Any]]:
    data = read_metadata(metadata_path)
    return data.get(pdf_id)


def upsert_pdf_record(metadata_path: Path, pdf_id: str, record: Dict[str, Any]) -> None:
    data = read_metadata(metadata_path)
    data[pdf_id] = record
    write_metadata(metadata_path, data)


def list_pdf_records(metadata_path: Path) -> Dict[str, Any]:
    return read_metadata(metadata_path)
