import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Home.css';
import TeacherModal from './TeacherModal';

const Home = () => {
  const [info, setInfo] = useState(null);
  const [aiResult, setAiResult] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [toast, setToast] = useState({ show: false, msg: '' });
  const [selectedTeacher, setSelectedTeacher] = useState(null);

  // LOGIKA URL FLEKSIBEL: Otomatis deteksi Lokal atau Production (Railway)
  const API_BASE_URL = process.env.NODE_ENV === 'production' 
    ? 'https://sonata-music-school-production.up.railway.app' 
    : 'http://localhost:5000';

  useEffect(() => {
    // Mengambil data info sekolah dan daftar guru
    axios.get(`${API_BASE_URL}/api/info`)
      .then(res => setInfo(res.data))
      .catch(err => {
        console.error(err);
        triggerToast("Gagal mengambil data dari server.");
      });
  }, [API_BASE_URL]);

  const triggerToast = (msg) => {
    setToast({ show: true, msg });
    setTimeout(() => setToast({ show: false, msg: '' }), 3000);
  };

  const analyzeVoiceLive = () => {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = audioContext.createAnalyser();
    
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
      const source = audioContext.createMediaStreamSource(stream);
      source.connect(analyser);
      analyser.fftSize = 256;
      const bufferLength = analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      setIsRecording(true);
      setAiResult('');
      triggerToast("AI sedang mendengarkan suaramu... 🎤");

      setTimeout(async () => {
        analyser.getByteFrequencyData(dataArray);
        const avgFrequency = dataArray.reduce((a, b) => a + b) / bufferLength;
        const pitchSimulated = Math.min(Math.max(Math.round(avgFrequency / 10), 1), 10);
        const powerSimulated = Math.min(Math.max(Math.round(Math.max(...dataArray) / 20), 1), 10);

        try {
          // Menggunakan API_BASE_URL agar tetap jalan di Vercel
          const res = await axios.post(`${API_BASE_URL}/api/predict-vocal`, {
            pitch: pitchSimulated,
            power: powerSimulated
          });
          setAiResult(res.data.message);
        } catch (err) {
          triggerToast("Gagal memproses suara.");
        } finally {
          setIsRecording(false);
          stream.getTracks().forEach(track => track.stop());
        }
      }, 3000); 
    }).catch(() => triggerToast("Izin mikrofon ditolak!"));
  };

  if (!info) return <div className="loading">Loading Sonata Music School...</div>;

  return (
    <div className="page">
      {toast.show && <div className="mini-toast">{toast.msg}</div>}

      <div className="hero-section">
        <h2>Tentang Kami</h2>
        <p className="vision-text">{info.vision}</p>
        <p className="address">📍 {info.contact}</p>
      </div>
      
      {/* SEKSI TABEL GURU */}
      <div className="table-section">
        <h3>Riwayat Guru & Spesialisasi</h3>
        <table className="table-custom">
          <thead>
            <tr>
              <th>Nama Guru (Klik untuk Detail)</th>
              <th>Kelas (Genre)</th>
              <th>Spesialisasi Alat</th>
            </tr>
          </thead>
          <tbody>
            {info.teachers.map(t => (
              <tr key={t.id}>
                <td 
                  onClick={() => setSelectedTeacher(t)} 
                  className="teacher-name-link"
                >
                  {t.name}
                </td>
                <td>{t.genre}</td>
                <td>{t.instrument}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* RENDER MODAL ROCKER */}
      {selectedTeacher && (
        <TeacherModal 
          teacher={selectedTeacher} 
          onClose={() => setSelectedTeacher(null)} 
        />
      )}

      {/* SEKSI AI & RADIO */}
      <div className="flex-container">
        <div className="info-card ai-card">
          <div className="card-content">
            <h3>🎙️ AI Vocal Diagnostic</h3>
            <p>Penasaran karakter vokalmu cocok di kelas mana?</p>
            <button 
              className={`btn-record ${isRecording ? 'recording' : ''}`} 
              onClick={analyzeVoiceLive}
              disabled={isRecording}
            >
              {isRecording ? '⌛ ANALYZING...' : '🔴 MULAI TES VOKAL'}
            </button>
            {aiResult && <div className="ai-result-tag">{aiResult}</div>}
          </div>
        </div>

        <div className="info-card radio-card">
          <div className="card-content">
            <h3>🎵 Sonata Radio</h3>
            <div className="video-container">
              <iframe
                src="https://www.youtube.com/embed/ctkuJsh-tGQ"
                title="Sonata Radio"
                frameBorder="0"
                allow="autoplay; encrypted-media"
                allowFullScreen
              ></iframe>
            </div>
            <p className="music-sub">Streaming: Still I'm Sure We'll Love Again</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;