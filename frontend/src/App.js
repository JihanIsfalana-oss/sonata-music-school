import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './components/Home';      // Pastikan path sesuai
import Register from './components/Register'; // Pastikan path sesuai
import Students from './components/Students'; // Pastikan path sesuai
import ChatbotSonata from './components/ChatbotSonata';
import Curriculum from './components/Curriculum';
import './App.css';

function App() {
  // Logic untuk Custom Cursor
  const [cursorPosition, setCursorPosition] = useState({ x: 0, y: 0 });
  const [cursorActive, setCursorActive] = useState(false);

  useEffect(() => {
    const moveCursor = (e) => {
      setCursorPosition({ x: e.clientX, y: e.clientY });
    };

    // Efek saat klik mouse
    const mouseDown = () => setCursorActive(true);
    const mouseUp = () => setCursorActive(false);

    window.addEventListener('mousemove', moveCursor);
    window.addEventListener('mousedown', mouseDown);
    window.addEventListener('mouseup', mouseUp);

    return () => {
      window.removeEventListener('mousemove', moveCursor);
      window.removeEventListener('mousedown', mouseDown);
      window.removeEventListener('mouseup', mouseUp);
    };
  }, []);

  // ... (Kode import dan logic cursor di atas tetap sama)

  return (
    <Router>
      <div className="bg-layer"></div>
      
      <div 
        className={`cursor-glow ${cursorActive ? 'active' : ''}`}
        style={{ left: cursorPosition.x, top: cursorPosition.y }}
      ></div>

      <div className="app-container">
      <nav className="navbar">
        <h1>SONATA MUSIC SCHOOL</h1>
        <div className="links">
          <Link to="/">Home</Link>
          <Link to="/register">Join Class</Link>
          <Link to="/students">Students</Link>
          <Link to="/curriculum">Curriculum</Link>
        </div>
      </nav>

      <div className="content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/students" element={<Students />} />
          <Route path="/curriculum" element={<Curriculum />} />
        </Routes>
      </div>


      <footer className="footer-rock">
        <p>
          &copy; 2026 Created by <span className="neon-name">Mochammad Jihan Isfalana</span>
        </p>
      </footer>
    </div>
    
    {/* Hapus <ChatBot /> yang lama agar tidak double tombol di layar */}
    <ChatbotSonata /> 
    </Router>
  );
}

export default App;