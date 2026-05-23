"""
ingest.py — Read PDFs from docs/, chunk them, embed with sentence-transformers, store in FAISS.

Run once (or re-run whenever you add new PDFs):
    python ingest.py
"""

import os
import pickle
import numpy as np
import faiss
from pathlib import Path
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from utils import chunk_text


DOCS_DIR = "docs"
FAISS_INDEX_PATH = "faiss.index"
CHUNKS_PATH = "chunks.pkl"
EMBED_MODEL = "all-MiniLM-L6-v2"
EMBED_DIM = 384


def extract_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def embed(texts: list[str], model: SentenceTransformer) -> np.ndarray:
    vectors = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    return vectors.astype("float32")


def build_index():
    pdf_files = list(Path(DOCS_DIR).glob("*.pdf"))

    if not pdf_files:
        print(f"No PDFs found in ./{DOCS_DIR}/  — add some PDFs and re-run.")
        return

    print(f"Found {len(pdf_files)} PDF(s): {[f.name for f in pdf_files]}\n")

    all_chunks = []
    for pdf_file in pdf_files:
        print(f"Reading {pdf_file.name}...")
        text = extract_text(str(pdf_file))
        chunks = chunk_text(text, pdf_file.name)
        all_chunks.extend(chunks)
        print(f"  → {len(chunks)} chunks")

    print(f"\nTotal chunks: {len(all_chunks)}")
    print("Loading embedding model (downloads ~90MB on first run)...")

    model = SentenceTransformer(EMBED_MODEL)
    texts = [c["text"] for c in all_chunks]

    print("Embedding chunks...")
    vectors = embed(texts, model)

    # Normalise so inner product == cosine similarity
    faiss.normalize_L2(vectors)
    index = faiss.IndexFlatIP(EMBED_DIM)
    index.add(vectors)

    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(all_chunks, f)

    print(f"\nSaved {index.ntotal} vectors → {FAISS_INDEX_PATH}")
    print(f"Saved chunks → {CHUNKS_PATH}")
    print("\nDone! Now run:  streamlit run app.py")


if __name__ == "__main__":
    build_index()
