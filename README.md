# Enterprise RAG Chatbot

An Enterprise Retrieval-Augmented Generation (RAG) chatbot that enables users to interact with PDF documents using natural language. The system retrieves relevant information from uploaded documents using FAISS vector search and generates context-aware responses using Groq's Llama 3.3 70B model.

---

## 🚀 Overview

Traditional chatbots rely only on pre-trained knowledge and cannot access information stored in private documents. This project implements a Retrieval-Augmented Generation (RAG) pipeline that allows users to chat with their PDF documents.

The chatbot:

* Extracts text from PDFs
* Splits text into manageable chunks
* Generates embeddings using Sentence Transformers
* Stores embeddings in a FAISS vector database
* Retrieves relevant document chunks for a query
* Uses Groq's Llama 3.3 70B model to generate answers

---

## ✨ Features

* 📄 PDF document ingestion
* 🔍 Semantic search with FAISS
* 🤖 Context-aware question answering
* ⚡ Fast inference using Groq API
* 🖥️ Streamlit-based web interface
* 💻 Runs locally without GPU
* 📚 Supports multiple PDF documents

---

## 🏗️ System Architecture

```text
PDF Documents
      │
      ▼
Text Extraction
      │
      ▼
Text Chunking
      │
      ▼
Sentence Embeddings
(all-MiniLM-L6-v2)
      │
      ▼
FAISS Vector Store
      │
      ▼
User Query
      │
      ▼
Similarity Search
      │
      ▼
Relevant Chunks
      │
      ▼
Groq Llama 3.3 70B
      │
      ▼
Generated Answer
```

---

## 🛠️ Tech Stack

| Component       | Technology       |
| --------------- | ---------------- |
| Language        | Python           |
| Frontend        | Streamlit        |
| Vector Database | FAISS            |
| Embedding Model | all-MiniLM-L6-v2 |
| LLM Provider    | Groq             |
| LLM             | Llama 3.3 70B    |
| PDF Processing  | PyPDF            |
| Storage         | Pickle           |

---

## 📂 Project Structure

```bash
Enterprise-RAG-Chatbot/
│
├── app.py                # Streamlit application
├── ingest.py             # PDF ingestion & indexing
├── retrieve.py           # Semantic retrieval
├── generate.py           # LLM response generation
├── utils.py              # Utility functions
│
├── docs/                 # PDF documents
│   ├── sample1.pdf
│   └── sample2.pdf
│
├── faiss.index           # Generated vector index
├── chunks.pkl            # Stored document chunks
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MIRUDHULA-DHANARAJ/Enterprise-RAG-Chatbot.git

cd Enterprise-RAG-Chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Groq API Setup

1. Create an account at https://console.groq.com
2. Generate a free API key
3. Copy the API key

Example:

```text
gsk_xxxxxxxxxxxxxxxxxxxxxxxxx
```

4. Paste the key into the Streamlit sidebar after launching the application

---

## ▶️ Running the Project

### Step 1: Add PDF Files

Place your PDF documents inside the `docs/` folder.

```text
docs/
├── company_policy.pdf
├── handbook.pdf
└── product_manual.pdf
```

### Step 2: Build the Vector Index

```bash
python ingest.py
```

This creates:

```text
faiss.index
chunks.pkl
```

### Step 3: Launch the Application

```bash
streamlit run app.py
```

Open in browser:

```text
http://localhost:8501
```

---

## 💬 Example Questions

* What is the company's leave policy?
* Summarize this document.
* What are the key responsibilities mentioned?
* Explain the onboarding process.
* What are the product specifications?

---

## 📈 Future Improvements

* Chat history memory
* Source citations
* Multi-document comparison
* User authentication
* Cloud deployment
* Hybrid retrieval (BM25 + Vector Search)
* Support for DOCX and PPTX files

---

## 🎯 Learning Outcomes

This project demonstrates:

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases (FAISS)
* Embedding Models
* Large Language Model Integration
* Prompt Engineering
* Streamlit Development

---

## 👩‍💻 Author

**Mirudhula D**

B.Tech Artificial Intelligence and Data Science

Interested in Data Science, Machine Learning, Generative AI, and Intelligent Information Retrieval Systems.

---

## ⭐ If you found this project useful, consider giving it a star!
