"""
utils.py — Text chunking helper used by ingest.py
"""

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def chunk_text(text: str, filename: str) -> list[dict]:
    """
    Split text into overlapping chunks.
    Returns list of dicts with text, source filename, and chunk index.
    """
    chunks = []
    start = 0
    index = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()

        if chunk:
            chunks.append({
                "text": chunk,
                "source": filename,
                "chunk_index": index,
            })
            index += 1

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks
