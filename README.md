# Enterprise RAG Chatbot

An enterprise-grade Retrieval-Augmented Generation (RAG) chatbot that enables users to query PDF documents using natural language. The system combines dense vector retrieval, BM25 keyword search, and cross-encoder reranking to deliver accurate, context-aware responses while minimizing hallucinations.

Live Demo : https://enterprise-rag-ai.streamlit.app/
## 🚀 Features

- PDF document ingestion and processing
- Intelligent text chunking
- Dense semantic retrieval using FAISS
- BM25 keyword-based retrieval
- Hybrid search (Dense + Sparse Retrieval)
- Cross-Encoder reranking for improved relevance
- Context-aware answer generation using LLMs
- Streamlit-based user interface
- Multi-document question answering
- Low-latency inference through Groq API

---

## 📌 Problem Statement

Large Language Models possess strong reasoning capabilities but lack access to private organizational knowledge. This project addresses that limitation by implementing a Retrieval-Augmented Generation (RAG) pipeline that grounds LLM responses using enterprise documents.

The chatbot retrieves the most relevant information from uploaded PDFs before generating responses, resulting in more accurate and reliable answers.

---

## 🏗 System Architecture

```text
PDF Documents
      │
      ▼
Document Processing
      │
      ▼
Text Chunking
      │
      ▼
Embedding Generation
(all-MiniLM-L6-v2)
      │
      ▼
FAISS Vector Store
      │
      ├───────────────┐
      ▼               ▼
Dense Search      BM25 Search
      │               │
      └───────┬───────┘
              ▼
      Hybrid Retrieval
              │
              ▼
 Cross-Encoder Reranking
              │
              ▼
      Top Relevant Chunks
              │
              ▼
      Groq Llama 3.3 70B
              │
              ▼
       Generated Answer
```

---

## ⚙️ Technology Stack

| Component | Technology |
|------------|------------|
| Language | Python |
| Frontend | Streamlit |
| Vector Store | FAISS |
| Embedding Model | Sentence Transformers |
| Dense Retrieval | all-MiniLM-L6-v2 |
| Sparse Retrieval | BM25 |
| Reranker | Cross-Encoder |
| LLM Provider | Groq |
| LLM | Llama 3.3 70B |
| Document Processing | PyPDF |
| Storage | Pickle |

---

## 📂 Project Structure

```bash
Enterprise-RAG-Chatbot/
│
├── app.py                # Streamlit application
├── ingest.py             # Document ingestion and indexing
├── retrieve.py           # Hybrid retrieval pipeline
├── generate.py           # LLM response generation
├── utils.py              # Helper functions
│
├── docs/                 # PDF documents
│
├── faiss.index           # Dense vector index
├── chunks.pkl            # Stored document chunks
│
├── requirements.txt
└── README.md
```

---

## 🔧 Installation

### Clone Repository

```bash
git clone https://github.com/MIRUDHULA-DHANARAJ/Enterprise-RAG-Chatbot.git

cd Enterprise-RAG-Chatbot
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Groq API Setup

1. Create an account at https://console.groq.com
2. Generate an API key
3. Copy your key

```text
gsk_xxxxxxxxxxxxxxxxxxxxxxxxx
```

4. Enter the key in the Streamlit sidebar after launching the application.

---

## ▶️ Running the Project

### Step 1: Add Documents

Place PDF files inside the `docs/` directory.

```text
docs/
├── employee_handbook.pdf
├── company_policy.pdf
└── product_manual.pdf
```

### Step 2: Build Indexes

```bash
python ingest.py
```

This creates:

```text
faiss.index
chunks.pkl
```

### Step 3: Launch Application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## 💬 Example Queries

- What is the company's leave policy?
- Summarize the onboarding process.
- What responsibilities are assigned to project managers?
- Explain the product specifications.
- What are the compliance requirements mentioned in the handbook?

---

## 📈 Performance Improvements

The system incorporates several retrieval enhancements:

- Hybrid retrieval combining FAISS and BM25
- Cross-encoder reranking of retrieved candidates
- Context-grounded answer generation
- Reduced hallucinations through retrieval augmentation
- Improved retrieval precision compared to standalone vector search

---

## 🎯 Learning Outcomes

This project demonstrates practical experience in:

- Retrieval-Augmented Generation (RAG)
- Dense and Sparse Information Retrieval
- Vector Databases (FAISS)
- Transformer Embeddings
- Cross-Encoder Reranking
- Large Language Model Integration
- Prompt Engineering
- Streamlit Application Development

---

## 🔮 Future Enhancements

- Conversational memory
- Source citation highlighting
- Document upload through UI
- Multi-format document support (DOCX, PPTX)
- Cloud deployment
- User authentication
- Feedback-driven retrieval optimization

---

## 👩‍💻 Author

**Mirudhula D**

B.Tech Artificial Intelligence and Data Science

Aspiring Data Scientist with interests in Generative AI, Information Retrieval, Machine Learning, and Intelligent Knowledge Systems.

---

⭐ If you found this project useful, consider starring the repository.
