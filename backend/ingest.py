import json
import os

def chunk_text(text):
    paragraphs = text.split("\n\n")
    chunks = []

    for paragraph in paragraphs:
        cleaned = paragraph.strip()

        if cleaned != "":
            chunks.append(cleaned)

    return chunks


def ingest_all_notes(folder_path="data"):
    chunk_data = []
    chunk_id = 0

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                content = file.read()

            chunks = chunk_text(content)

            for chunk in chunks:
                chunk_data.append({
                    "id": chunk_id,
                    "text": chunk,
                    "source": file_path
                })
                chunk_id += 1

    

    with open("data/chunks.json", "w") as file:
        json.dump(chunk_data, file, indent=4)

    return chunk_data