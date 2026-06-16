import { useState } from 'react'
import './App.css'

// Base URL for your FastAPI backend
const API_BASE = 'http://127.0.0.1:8000'

function App() {
  // Which mode is active: "ask", "study-guide", or "upload"
  const [mode, setMode] = useState('ask')

  // What the user typed in the input box
  const [input, setInput] = useState('')

  // File selected for upload
  const [selectedFile, setSelectedFile] = useState(null)

  // The text shown in the results card (answer or study guide)
  const [result, setResult] = useState('')

  // Source chunks returned by the API
  const [sources, setSources] = useState([])

  // True while waiting for the API response
  const [loading, setLoading] = useState(false)

  // Error message if the request fails
  const [error, setError] = useState('')

  // Call the backend when the user clicks Generate / Ask
  async function handleSubmit(event) {
    event.preventDefault()

    const trimmed = input.trim()
    if (!trimmed) return

    setLoading(true)
    setError('')
    setResult('')
    setSources([])

    try {
      let url

      if (mode === 'ask') {
        // Ask Question endpoint
        url = `${API_BASE}/ask?query=${encodeURIComponent(trimmed)}`
      } else {
        // Generate Study Guide endpoint
        url = `${API_BASE}/study-guide?topic=${encodeURIComponent(trimmed)}`
      }

      const response = await fetch(url)

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      const data = await response.json()

      // The API returns "answer" for questions and "study_guide" for guides
      if (mode === 'ask') {
        setResult(data.answer)
      } else {
        setResult(data.study_guide)
      }

      setSources(data.sources || [])
    } catch (err) {
      setError(
        'Could not reach the backend. Make sure FastAPI is running at http://127.0.0.1:8000'
      )
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  // Send a file to POST /upload
  async function handleUpload(event) {
    event.preventDefault()

    if (!selectedFile) return

    setLoading(true)
    setError('')
    setResult('')
    setSources([])

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      const data = await response.json()

      setResult(
        `${data.message}\n\nFile: ${data.filename}\nChunks in knowledge base: ${data.num_chunks}`
      )
      setSelectedFile(null)
      event.target.reset()
    } catch (err) {
      setError(
        'Upload failed. Make sure FastAPI is running at http://127.0.0.1:8000'
      )
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const inputLabel =
    mode === 'ask' ? 'Your question' : 'Topic for study guide'

  const inputPlaceholder =
    mode === 'ask'
      ? 'e.g. What is AWS Lambda?'
      : 'e.g. AWS S3 storage basics'

  const buttonLabel = mode === 'ask' ? 'Ask' : 'Generate'

  return (
    <div className="dashboard">
      <header className="header">
        <h1 className="title">StudyBuddy</h1>
        <p className="subtitle">AI-powered study coach</p>
      </header>

      {/* Switch between Ask Question and Generate Study Guide */}
      <div className="tabs">
        <button
          type="button"
          className={`tab ${mode === 'ask' ? 'active' : ''}`}
          onClick={() => setMode('ask')}
        >
          Ask Question
        </button>
        <button
          type="button"
          className={`tab ${mode === 'study-guide' ? 'active' : ''}`}
          onClick={() => setMode('study-guide')}
        >
          Generate Study Guide
        </button>
        <button
          type="button"
          className={`tab ${mode === 'upload' ? 'active' : ''}`}
          onClick={() => setMode('upload')}
        >
          Upload Notes
        </button>
      </div>

      {/* Upload form */}
      {mode === 'upload' ? (
        <form className="input-card" onSubmit={handleUpload}>
          <label className="input-label" htmlFor="file-input">
            Add a .txt or .pdf file to your notes
          </label>
          <input
            id="file-input"
            className="file-input"
            type="file"
            accept=".txt,.pdf"
            onChange={(e) => setSelectedFile(e.target.files[0] || null)}
          />
          {selectedFile && (
            <p className="file-name">Selected: {selectedFile.name}</p>
          )}
          <button
            className="submit-btn"
            type="submit"
            disabled={loading || !selectedFile}
          >
            {loading ? 'Uploading…' : 'Upload'}
          </button>
        </form>
      ) : (
        /* Ask / Study Guide form */
        <form className="input-card" onSubmit={handleSubmit}>
          <label className="input-label" htmlFor="user-input">
            {inputLabel}
          </label>
          <input
            id="user-input"
            className="input-field"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={inputPlaceholder}
          />
          <button className="submit-btn" type="submit" disabled={loading}>
            {loading ? 'Loading…' : buttonLabel}
          </button>
        </form>
      )}

      {/* Results card */}
      <section className={`results-card ${!result && !loading && !error ? 'empty' : ''}`}>
        <h2 className="results-heading">Results</h2>

        {loading && (
          <p className="loading">
            <span className="loading-dot" />
            <span className="loading-dot" />
            <span className="loading-dot" />
            {mode === 'upload' ? 'Uploading…' : 'Thinking…'}
          </p>
        )}

        {error && <p className="error-message">{error}</p>}

        {!loading && !error && result && (
          <p className="results-text">{result}</p>
        )}

        {!loading && !error && !result && (
          <p>
            {mode === 'upload'
              ? 'Upload status will appear here.'
              : 'Your answer or study guide will appear here.'}
          </p>
        )}
      </section>

      {/* Sources from your notes */}
      {sources.length > 0 && (
        <section className="sources-card">
          <h2 className="sources-heading">Sources</h2>
          <ul className="sources-list">
            {sources.map((source, index) => (
              <li key={index} className="source-item">
                {source}
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}

export default App
