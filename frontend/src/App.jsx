import { useState } from "react"
import Uploader from "./components/Uploader"
import ChatBox from "./components/ChatBox"
import "./App.css"

function App() {
  const [sessionId, setSessionId] = useState(null)
  const [filename, setFilename] = useState(null)

  return (
    <div className="app">
      <header>
        <h1>📄 SmartDoc</h1>
        <p>Upload a document and ask anything about it</p>
      </header>

      <main>
        {!sessionId ? (
          <Uploader onUpload={(id, name) => {
            setSessionId(id)
            setFilename(name)
          }} />
        ) : (
          <ChatBox
            sessionId={sessionId}
            filename={filename}
            onReset={() => {
              setSessionId(null)
              setFilename(null)
            }}
          />
        )}
      </main>
    </div>
  )
}

export default App