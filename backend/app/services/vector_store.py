from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pathlib import Path
import pickle

model = SentenceTransformer("all-MiniLM-L6-v2")

DATA_DIR = Path("backend/app/data")


def _index_path(pdf_id: str) -> Path:
    return DATA_DIR / f"{pdf_id}_faiss_index.bin"


def _doc_path(pdf_id: str) -> Path:
    return DATA_DIR / f"{pdf_id}_faiss_docs.pkl"


def build_index(pdf_id: str, chunks: list):           # ← pdf_id added
    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(_index_path(pdf_id)))

    with open(_doc_path(pdf_id), "wb") as f:
        pickle.dump(chunks, f)


def search_index(pdf_id: str, query: str, k: int = 3) -> list:   # ← pdf_id added
    idx_path = _index_path(pdf_id)
    doc_path = _doc_path(pdf_id)

    if not idx_path.exists() or not doc_path.exists():
        return []

    index = faiss.read_index(str(idx_path))

    with open(doc_path, "rb") as f:
        docs = pickle.load(f)

    q_embedding = model.encode([query])
    distances, indices = index.search(np.array(q_embedding), k)

    results = [docs[i] for i in indices[0] if 0 <= i < len(docs)]
    return results