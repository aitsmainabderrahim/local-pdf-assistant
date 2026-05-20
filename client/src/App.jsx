import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Upload, FileText, Loader2 } from 'lucide-react';
import './App.css';

const API_URL = "http://localhost:8000";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [pdfUploaded, setPdfUploaded] = useState(false);
  const chatEndRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setIsUploading(true);
    try {
      await axios.post(`${API_URL}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setPdfUploaded(true);
      setMessages([{ role: "bot", content: "PDF uploaded successfully! What would you like to know about it?" }]);
    } catch (error) {
      alert("Error uploading file: " + (error.response?.data?.detail || error.message));
    } finally {
      setIsUploading(false);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || !pdfUploaded) return;

    const userMessage = input;
    setMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setInput("");
    setIsTyping(true);

    try {
      const response = await axios.post(`${API_URL}/chat`, { question: userMessage });
      setMessages(prev => [...prev, { role: "bot", content: response.data.answer }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: "bot", content: "Error: Could not get an answer." }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>PDF AI Assistant</h1>
        <div className="upload-container">
          <input 
            type="file" 
            id="pdf-upload" 
            accept=".pdf" 
            onChange={handleFileUpload} 
            disabled={isUploading}
          />
          <label htmlFor="pdf-upload" className={`upload-btn ${isUploading ? 'loading' : ''}`}>
            {isUploading ? <Loader2 className="spinner"/> : <Upload size="{18}"/>}
            {isUploading ? "Processing..." : "Upload PDF"}
          </label>
        </div>
      </header>

      <main className="chat-container">
        {!pdfUploaded && messages.length === 0 ? (
          <div className="empty-state">
            <FileText size="{48}" className="icon-empty"/>
            <h2>Welcome to PDF AI</h2>
            <p>Please upload a PDF document to start chatting.</p>
          </div>
        ) : (
          <div className="messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message-wrapper ${msg.role}`}>
                <div className="message">{msg.content}</div>
              </div>
            ))}
            {isTyping && (
              <div className="message-wrapper bot">
                <div className="message typing">
                  <span className="dot"></span><span className="dot"></span><span className="dot"></span>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
        )}
      </main>

      <form className="input-area" onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={pdfUploaded ? "Ask a question..." : "Upload a PDF first..."}
          disabled={!pdfUploaded || isTyping}
        />
        <button type="submit" disabled={!pdfUploaded || !input.trim() || isTyping}>
          <Send size="{18}"/>
        </button>
      </form>
    </div>
  );
}

export default App;