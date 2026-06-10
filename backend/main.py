from fastapi import FastAPI
from backend.ingest import ingest_note
from backend.search import search_chunks
from backend.vector_store import add_chunks_to_chroma, semantic_search

app = FastAPI()

# break into chunks 
def chunk_text(text):
    paragraphs = text.split("\n\n")
    chunks = []
    for paragraph in paragraphs:
        cleaned = paragraph.strip()

        if cleaned != "":
            chunks.append(cleaned)
    return chunks

# main route 
@app.get("/")
def root():
    return {"message": "StudyBuddy is running!"}

# reads txt files 
@app.get("/note")
def get_notes():
    with open("data/aws.txt", "r") as file:
        content = file.read()
    return {"note": content}

# reading and chunking 
@app.get("/chunks")
def get_chunks():
    with open("data/aws.txt", "r") as file:
        content = file.read()

    chunks = chunk_text(content)

    return {
        "num_chunks": len(chunks),
        "chunks": chunks
    }

@app.get("/ingest")
def ingest():
    chunks = ingest_note("data/aws.txt")

    return {
        "message": "Note ingested successfully!",
        "num_chunks": len(chunks),
        "chunks": chunks
    }

@app.get("/search")
def search(query: str):
    results = search_chunks(query)

    return {
        "query": query,
        "num_results": len(results),
        "results": results
    }

@app.get("/vectorize")
def vectorize():
    num_chunks = add_chunks_to_chroma()

    return {
        "message": "Chunks added to ChromaDB!",
        "num_chunks": num_chunks
    }


@app.get("/semantic-search")
def semantic_search_route(query: str):
    results = semantic_search(query)

    return {
        "query": query,
        "documents": results["documents"][0]
    }