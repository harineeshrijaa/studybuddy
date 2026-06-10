import json

def chunk_text(text, chunk_size=200, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def ingest_note(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    chunks = chunk_text(content)

    chunk_data = []

    for i, chunk in enumerate(chunks):
        chunk_data.append({
            "id": i,
            "text": chunk,
            "source": file_path
        })

    with open("data/chunks.json", "w") as file:
        json.dump(chunk_data, file, indent=4)

    return chunk_data