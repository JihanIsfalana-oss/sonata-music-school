import React, { useState, useEffect, useRef } from 'react';
import './ChatBot.css'; // Kita akan buat file CSS khusus ini

const ChatBot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { text: "Yo! Saya Maestro Jihan. Siap menggebrak panggung musik hari ini?", sender: 'maestro' }
  ]);
  const messagesEndRef = useRef(null);

  // Auto scroll ke bawah setiap ada pesan baru
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
    // Mencegah scroll pada halaman utama saat chat terbuka
    document.body.style.overflow = !isOpen ? 'hidden' : 'auto';
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { text: input, sender: 'user' };
    setMessages(prev => [...prev, userMsg]);
    setInput('');

    try {
      const response = await fetch('https://sonata-music-school-production.up.railway.app/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });
      const data = await response.json();
      setMessages(prev => [...prev, { text: data.response, sender: 'maestro' }]);
    } catch (error) {
      setMessages(prev => [...prev, { text: "Koneksi ke backstage terputus!", sender: 'maestro' }]);
    }
  };

  return (
    <>
      {/* Tombol FAB (Floating Action Button) */}
      {!isOpen && (
        <div className="chat-fab" onClick={toggleChat}>
          <span className="fab-icon">🎸</span>
          <span className="fab-text">Tanya Maestro</span>
        </div>
      )}

      {/* Fullscreen Overlay */}
      <div className={`chat-fullscreen ${isOpen ? 'active' : ''}`}>
        <div className="chat-header">
          <div className="header-info">
            <span className="maestro-status"></span>
            <h2>MAESTRO JIHAN</h2>
          </div>
          <button className="close-btn" onClick={toggleChat}>&times;</button>
        </div>

        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message-bubble ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-area">
          <input 
            type="text" 
            autoFocus
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Tulis pesan untuk Maestro..."
          />
          <button onClick={sendMessage}>KIRIM 🤘</button>
        </div>
      </div>
    </>
  );
};

export default ChatBot;