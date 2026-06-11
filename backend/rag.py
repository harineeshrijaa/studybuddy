import os
from dotenv import load_dotenv
from google import genai
from backend.vector_store import semantic_search

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def answer_question(query):
    results = semantic_search(query, num_results=2)
    documents = results["documents"][0]

    context = "\n\n".join(documents)

    prompt = f"""
You are StudyBuddy, a helpful AI study assistant.

Answer the user's question using ONLY the context below.
If the answer is not in the context, say:
"I don't know based on your notes yet."

Context:
{context}

Question:
{query}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return {
        "question": query,
        "answer": response.text,
        "sources": documents
    }