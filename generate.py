"""
generate.py — Send RAG prompt to Groq's free API (Llama 3.3 70B).

No download. No storage. Faster than local phi3. Free tier:
  • 14,400 requests / day
  • 6,000 tokens / minute

Get your free key at: https://console.groq.com
"""

import os
import requests


GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"   # free, fast, high quality



def generate(query: str, chunks: list[dict], api_key: str = None) -> str:
    """
    Build a RAG prompt from the chunks and call Groq.
    api_key can be passed directly (from UI) or read from env.
    """
    key = api_key or os.getenv("GROQ_API_KEY", "")
    if not key:
        return (
            "⚠️ No Groq API key found.\n\n"
            "Get a free key at https://console.groq.com\n"
            "Then paste it in the sidebar."
        )

    # Build numbered context from retrieved chunks
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(f"[Source {i} — {chunk['source']}]\n{chunk['text']}")
    context = "\n\n".join(context_parts)

    prompt = (
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        f"Answer using ONLY the context above. "
        f"Cite sources as [Source N] inline. "
        f"If the answer isn't in the context, say so."
    )

    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a precise assistant. Answer only from the provided context. Be concise."
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "max_tokens": 1024,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except requests.exceptions.ConnectionError:
        return "❌ Network error — check your internet connection."
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            return "❌ Invalid API key. Check your key at https://console.groq.com"
        if response.status_code == 429:
            return "⚠️ Rate limit hit. Wait a minute and try again (free tier: 6k tokens/min)."
        return f"❌ Groq API error: {e}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"


if __name__ == "__main__":
    dummy_chunks = [
        {
            "text": "RAG stands for Retrieval Augmented Generation. It grounds LLM answers in real documents.",
            "source": "notes.pdf",
            "chunk_index": 0,
        },
        {
            "text": "FAISS is Meta's library for fast similarity search over millions of vectors.",
            "source": "paper1.pdf",
            "chunk_index": 2,
        },
    ]

    query = "What is RAG and what is FAISS?"

    if not os.getenv("GROQ_API_KEY"):
        print("Set GROQ_API_KEY to test:  export GROQ_API_KEY=gsk_...")
    else:
        print(f"Query: {query}\n")
        answer = generate(query, dummy_chunks)
        print(f"Answer:\n{answer}")
