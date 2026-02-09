import React, { useState, useEffect, useRef } from 'react';
import './ChatbotSonata.css'; 

const ChatbotSonata = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  // State pesan awal
  const [messages, setMessages] = useState([
    { text: "Yo! Saya Maestro Jihan. Siap menggebrak panggung musik hari ini?", sender: 'maestro' }
  ]);
  const messagesEndRef = useRef(null);

  // Auto scroll ke bawah setiap ada pesan baru
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isOpen]); // Tambahkan isOpen agar saat dibuka langsung scroll bawah

  const toggleChat = () => {
    setIsOpen(!isOpen);
    // Mencegah scroll pada halaman utama saat chat terbuka (opsional, sesuaikan selera)
    // document.body.style.overflow = !isOpen ? 'hidden' : 'auto'; 
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    // 1. Tampilkan pesan user dulu di layar
    const userMsg = { text: input, sender: 'user' };
    setMessages(prev => [...prev, userMsg]);
    setInput(''); // Kosongkan input

    // --- LOGIKA URL (YANG SUDAH DIPERBAIKI) ---
    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    
    // PERBAIKAN PENTING:
    // Backend kamu menggunakan route '/test-chat', jadi production juga harus '/test-chat'
    const apiUrl = isLocal 
      ? 'http://127.0.0.1:8080/test-chat' 
      : 'https://sonata-music-school-production.up.railway.app/test-chat'; 

    try {
      // Set loading state dummy (opsional, biar ada feedback)
      // setMessages(prev => [...prev, { text: "Sedang menyetem gitar...", sender: 'maestro', isTemp: true }]);

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMsg.text }),
      });

      const data = await response.json();
      
      // Ambil jawaban dari key "reply" sesuai app.py
      const replyText = data.reply || "Mic-nya mati, cek koneksi lagi bro!";

      setMessages(prev => [...prev, { text: replyText, sender: 'maestro' }]);
      
    } catch (error) {
      console.error("Chat Error:", error);
      setMessages(prev => [...prev, { text: "Waduh, koneksi ke backstage (server) putus! Coba refresh.", sender: 'maestro' }]);
    }
  };

  // Handle enter key
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
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
            onKeyDown={handleKeyPress} // Ganti onKeyPress ke onKeyDown (lebih modern)
            placeholder="Tulis pesan untuk Maestro..."
          />
          <button onClick={sendMessage}>KIRIM 🤘</button>
        </div>
      </div>
    </>
  );
};

export default ChatbotSonata;