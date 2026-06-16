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

Formatting rules:
- Do not use markdown.
- Do not use **bold**.
- Use plain text.
- Use simple bullet points beginning with '-'.
- Keep answers easy to read.

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

def generate_study_guide(topic):
    results = semantic_search(topic, num_results=5)
    documents = results["documents"][0]

    context = "\n\n".join(documents)

    prompt = f"""
You are StudyBuddy, a helpful AI study assistant.

Create a clear, beginner-friendly study guide using ONLY the notes provided below.

The study guide should include:
1. A short overview of the topic
2. Key concepts and definitions
3. Important details to remember
4. Common confusion points or comparisons, if the notes support them
5. A quick summary
6. 3 practice questions

Rules:
- Use only the provided notes.
- Do not add outside information.
- If the notes do not contain enough information, say what is missing.
- Keep the explanation clear and organized.
- Do not assume the topic is about programming unless the notes show that.

Formatting rules:
- Do not use markdown.
- Do not use **bold**.
- Use plain text.
- Use simple bullet points beginning with '-'.
- Keep answers easy to read.

Notes:
{context}

Topic:
{topic}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return {
        "topic": topic,
        "study_guide": response.text,
        "sources": documents
    }