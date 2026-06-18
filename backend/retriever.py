from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DIR = "chroma_db"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


embeddings = HuggingFaceEmbeddings(
    model_name=EMBED_MODEL
)

vectorstore = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)


def retrieve(query: str):
    docs = retriever.invoke(query)

    results = []

    for doc in docs:
        results.append(
            {
                "text": doc.page_content,
                "source": doc.metadata.get("source"),
            }
        )

    return results


if __name__ == "__main__":
    query = "What is the main topic?"

    results = retrieve(query)

    for i, r in enumerate(results, start=1):
        print(f"\nResult {i}")
        print(f"Source: {r['source']}")
        print(r["text"][:300])