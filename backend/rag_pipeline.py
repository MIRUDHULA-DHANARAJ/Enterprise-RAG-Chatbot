from generate import generate

from .retriever import retrieve
from .memory import (
    add_user_message,
    add_assistant_message,
    get_history
)

from generate import generate
def ask(question: str, api_key: str):

    history = get_history()

    enhanced_query = f"""
Conversation History:
{history}

Current Question:
{question}
"""

    chunks = retrieve(enhanced_query)

    answer = generate(
        query=enhanced_query,
        chunks=chunks,
        api_key=api_key
    )

    add_user_message(question)
    add_assistant_message(answer)

    return {
        "answer": answer,
        "sources": chunks
    }

import os

if __name__ == "__main__":

    while True:

        question = input("\nYou: ")

        if question.lower() == "exit":
            break

        result = ask(
            question,
            api_key=os.getenv("GROQ_API_KEY")
        )

        print("\nBot:")
        print(result["answer"])