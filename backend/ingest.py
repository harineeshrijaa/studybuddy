import json
import os
from pypdf import PdfReader
from pypdf.errors import PdfStreamError

def chunk_text(text, chunk_size=120, overlap=25):
    text = text.replace("\n", " ")
    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def ingest_all_notes(folder_path="data"):
    chunk_data = []
    chunk_id = 0

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                content = file.read()
        elif filename.endswith(".pdf"):
            content = extract_pdf_text(file_path)
        else:
            continue
            
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

def extract_pdf_text(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text

    except PdfStreamError:
        print(f"Skipping corrupted PDF: {file_path}")
        return ""

    except Exception as e:
        print(f"Could not read PDF {file_path}: {e}")
        return ""
