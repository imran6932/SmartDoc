import { useState } from "react"
import axios from "axios"

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

function Uploader({ onUpload }) {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleUpload = async () => {
    if (!file) return
    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await axios.post(`${API_URL}/api/upload`, formData)
      onUpload(res.data.session_id, res.data.filename)
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="uploader">
      <div className="upload-box">
        <span className="upload-icon">📁</span>
        <p>Supported formats: PDF, DOCX, TXT</p>
        <input
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={(e) => setFile(e.target.files[0])}
        />
        {file && <p className="filename">Selected: {file.name}</p>}
        {error && <p className="error">{error}</p>}
        <button
          onClick={handleUpload}
          disabled={!file || loading}
        >
          {loading ? "Processing..." : "Upload & Analyse"}
        </button>
      </div>
    </div>
  )
}

export default Uploader