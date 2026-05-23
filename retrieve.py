"""
retrieve.py — Embed a query and find the top-k most relevant chunks from FAISS.
"""

import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


FAISS_INDEX_PATH = "faiss.index"
CHUNKS_PATH = "chunks.pkl"
EMBED_MODEL = "all-MiniLM-L6-v2"

# Keep model in memory across calls
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """
    Embed the query, search FAISS, return top_k chunk dicts
    (each has: text, source, chunk_index, score).
    """
    model = get_model()

    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

    query_vec = model.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(query_vec)

    scores, indices = index.search(query_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        chunk = chunks[idx].copy()
        chunk["score"] = float(score)
        results.append(chunk)

    return results


if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is the main topic?"

    try:
        results = retrieve(query)
        print(f"\nQuery: {query}\n")
        for i, r in enumerate(results, 1):
            print(f"[{i}] Score: {r['score']:.4f} | {r['source']} chunk {r['chunk_index']}")
            print(f"    {r['text'][:200]}...\n")
    except FileNotFoundError:
        print("Index not found. Run:  python ingest.py")
