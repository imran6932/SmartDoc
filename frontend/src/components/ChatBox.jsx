import { useState, useRef, useEffect } from "react"
import ReactMarkdown from "react-markdown"
import axios from "axios"

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

function ChatBox({ sessionId, filename, onReset }) {
  const [messages, setMessages] = useState([
    { role: "ai", text: `Document "${filename}" loaded. Ask me anything about it!` }
  ])
  const [question, setQuestion] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const clearSession = async () => {
  try {
    await axios.post(`${API_URL}/api/clear`, { session_id: sessionId })
    setMessages([
      { role: "ai", text: `Document **"${filename}"** loaded. Ask me anything about it!` }
    ])
  } catch (err) {
    console.error("Clear session failed", err)
  } finally {
    onReset()
  }
}

  const sendMessage = async () => {
    if (!question.trim() || loading) return

    const userMsg = { role: "user", text: question }
    setMessages(prev => [...prev, userMsg])
    setQuestion("")
    setLoading(true)

    try {
      const res = await axios.post(`${API_URL}/api/chat`, {
        session_id: sessionId,
        question: question
      })
      setMessages(prev => [...prev, { role: "ai", text: res.data.answer }])
    } catch (err) {
      const errorMsg = err.response?.data?.detail
        || err.message
        || "Something went wrong. Please try again."

      setError(`⚠️ ${errorMsg}`)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="chatbox">
      <div className="chat-header">
        <span>📄 {filename}</span>
        <button className="reset-btn" onClick={clearSession}>Clear Chat</button>
      </div>

      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <span className="bubble"><ReactMarkdown>{msg.text}</ReactMarkdown></span>
          </div>
        ))}
        {loading && (
          <div className="message ai">
            <span className="bubble typing">Thinking...</span>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="input-row">
        <textarea
          rows={2}
          placeholder="Ask a question about your document..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button onClick={sendMessage} disabled={!question.trim() || loading}>
          Send
        </button>
      </div>
        {error && <p className="error">{error}</p>}
    </div>
  )
}

export default ChatBox