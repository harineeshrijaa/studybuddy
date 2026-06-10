from fastapi import FastAPI
from backend.ingest import ingest_note
from backend.search import search_chunks

app = FastAPI()

# break into chunks 
def chunk_text(text, chunk_size=200, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

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