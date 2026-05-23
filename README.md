# RAG Chatbot — Groq API Version (Free + No Storage)

Chat with your PDFs using Llama 3.3 70B via Groq's free API.
No Ollama. No 2GB model download. No GPU needed.

## Free Groq limits
| What | Limit |
|------|-------|
| Requests | 14,400 / day |
| Speed | 6,000 tokens / min |
| Cost | $0 forever (free tier) |

## Setup (one time)

### 1. Get your free Groq API key
Go to **https://console.groq.com** → Sign up → API Keys → Create Key
Copy the key (starts with `gsk_`)

### 2. Create virtual environment
```bash
python -m venv venv

# Activate:
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install packages
```bash
pip install -r requirements.txt
```
~500MB total (sentence-transformers is the big one). No Ollama model needed.

## Run it

### Step 1 — Add PDFs
```
docs/
  your-file.pdf
  another.pdf
```

### Step 2 — Build the index
```bash
python ingest.py
```

### Step 3 — Launch
```bash
streamlit run app.py
```

Opens at **http://localhost:8501**

Paste your `gsk_...` key in the sidebar → start chatting.

## What runs where
| Component | Where |
|-----------|-------|
| PDF reading | your laptop |
| Embedding (all-MiniLM-L6-v2) | your laptop (CPU) |
| FAISS search | your laptop |
| LLM (Llama 3.3 70B) | Groq's servers (free API) |

## Files
```
rag-chatbot/
├── app.py          # Streamlit UI
├── ingest.py       # PDF → FAISS
├── retrieve.py     # Query → top chunks
├── generate.py     # Chunks → Groq → answer
├── utils.py        # Chunking
├── docs/           # Your PDFs here
├── faiss.index     # Auto-created by ingest.py
├── chunks.pkl      # Auto-created by ingest.py
└── requirements.txt
```
