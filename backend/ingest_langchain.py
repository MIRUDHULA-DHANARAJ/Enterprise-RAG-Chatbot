from pathlib import Path

from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


DOCS_DIR = "docs"
CHROMA_DIR = "chroma_db"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def extract_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def load_documents():
    documents = []

    pdf_files = list(Path(DOCS_DIR).glob("*.pdf"))

    for pdf in pdf_files:
        text = extract_text(str(pdf))

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": pdf.name
                }
            )
        )

    return documents


def build_vector_store():

    print("Loading PDFs...")

    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    
    split_docs = splitter.split_documents(docs)

    for idx, doc in enumerate(split_docs):
      doc.metadata["chunk_id"] = idx

    print(f"Created {len(split_docs)} chunks")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL
    )

    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    print("ChromaDB created successfully")
    print(f"Stored at: {CHROMA_DIR}")


if __name__ == "__main__":
    build_vector_store()