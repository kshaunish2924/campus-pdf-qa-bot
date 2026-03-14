from sentence_transformers import SentenceTransformer

# Load embedding model once (global)
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_chunks(chunks: list[str]):
    """
    Convert list of text chunks into vector embeddings.
    """

    embeddings = model.encode(chunks)

    return embeddings