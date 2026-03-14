import faiss
import numpy as np


def create_faiss_index(embeddings):
    """
    Create FAISS index from embeddings.
    """

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def search_index(index, query_embedding, top_k=3):
    """
    Search FAISS index for most similar chunks.
    """

    distances, indices = index.search(query_embedding, top_k)

    return distances, indices