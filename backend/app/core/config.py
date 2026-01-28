from pathlib import Path

# backend/app/data
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

UPLOAD_DIR = DATA_DIR / "uploads"
TEXT_DIR = DATA_DIR / "texts"
METADATA_PATH = DATA_DIR / "metadata.json"

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
TEXT_DIR.mkdir(parents=True, exist_ok=True)

# Ensure metadata file exists
if not METADATA_PATH.exists():
    METADATA_PATH.write_text("{}", encoding="utf-8")
