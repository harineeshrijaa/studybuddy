# StudyBuddy

StudyBuddy is a Retrieval-Augmented Generation (RAG) study assistant that allows users to upload notes, ask questions, and generate study guides from their own learning materials.

🌐 **Live Demo:**
https://studybuddy-2yra.onrender.com/

> **Note:** The application is hosted on Render's free tier. If the website is unavailable, the service may be sleeping or the free-tier instance may have expired. In that case, follow the instructions below to run the project locally.

---

## Features

* Upload `.txt` and `.pdf` study materials
* Ask questions grounded in your uploaded notes
* Generate AI-powered study guides
* Semantic search using vector embeddings
* Source-aware responses using Retrieval-Augmented Generation (RAG)
* Modern React frontend
* FastAPI backend
* Automatic knowledge base rebuilding on startup

---

## Tech Stack

### Frontend

* React
* Vite
* CSS

### Backend

* FastAPI
* ChromaDB
* Gemini API
* pypdf

### AI & Retrieval

* Retrieval-Augmented Generation (RAG)
* Vector Search
* Semantic Similarity Search
* Gemini LLM

---

## How It Works

1. Users upload PDF or text-based study materials.
2. StudyBuddy extracts the text content.
3. Documents are split into chunks.
4. Chunks are stored in ChromaDB as vector embeddings.
5. User questions are matched against the most relevant chunks.
6. Retrieved context is sent to Gemini.
7. Gemini generates an answer grounded in the uploaded materials.

---

## Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/harineeshrijaa/studybuddy.git
cd studybuddy
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Create Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

You can obtain a Gemini API key from Google AI Studio.

### 5. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 6. Build the Frontend

```bash
npm run build
cd ..
```

The React application will be bundled into the files served by FastAPI.

### 7. Run StudyBuddy

From the project root:

```bash
uvicorn backend.main:app --reload
```

### 8. Open the Application

Visit:

```text
http://127.0.0.1:8000
```

You should now be able to:

* Upload study materials
* Ask questions
* Generate study guides
* Explore your personal knowledge base

---

## Future Improvements

* Upload many file types
* Flashcard generation
* Quiz generation
* User authentication
* Cloud storage for uploaded notes
* Better PDF chunking strategies
* Source citations with page references
* Multi-document knowledge bases

---
