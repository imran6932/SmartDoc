import { useState, useRef, useEffect } from "react"
import axios from "axios"

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

function ChatBox({ sessionId, filename, onReset }) {
  const [messages, setMessages] = useState([
    { role: "ai", text: `Document "${filename}" loaded. Ask me anything about it!` }
  ])
  const [question, setQuestion] = useState("")
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

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
      setMessages(prev => [...prev, {
        role: "ai",
        text: "Sorry, something went wrong. Please try again."
      }])
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
        <button className="reset-btn" onClick={onReset}>Upload New</button>
      </div>

      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <span className="bubble">{msg.text}</span>
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
    </div>
  )
}

export default ChatBox