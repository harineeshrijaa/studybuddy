import json

def search_chunks(query):
    with open("data/chunks.json", "r") as file:
        chunks = json.load(file)

    results = []

    for chunk in chunks:
        if query.lower() in chunk["text"].lower():
            results.append(chunk)

    return results