import json
import chromadb

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection(name="study_notes")


def add_chunks_to_chroma():
    with open("data/chunks.json", "r") as file:
        chunks = json.load(file)

    for chunk in chunks:
        collection.add(
            ids=[str(chunk["id"])],
            documents=[chunk["text"]],
            metadatas=[{"source": chunk["source"]}]
        )

    return len(chunks)


def semantic_search(query, num_results=1):
    results = collection.query(
        query_texts=[query],
        n_results=num_results
    )

    return results