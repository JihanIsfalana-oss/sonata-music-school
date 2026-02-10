import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Curriculum.css';

const Curriculum = () => {
  const [modules, setModules] = useState([]);
  const [loading, setLoading] = useState(true);

  // Ambil data dari API backend kamu
  useEffect(() => {
    const fetchCurriculum = async () => {
      try {
        const response = await axios.get('https://sonata-music-school-production.up.railway.app/curriculum'); // Sesuaikan endpoint
        setModules(response.data);
        setLoading(false);
      } catch (error) {
        console.error("Gagal ambil data kurikulum", error);
        setLoading(false);
      }
    };
    fetchCurriculum();
  }, []);

  if (loading) return <div className="text-white text-center">Tuning instruments... 🎸</div>;

  return (
    <div className="curriculum-container">
      <header className="curriculum-header">
        <h1>Mastery Curriculum</h1>
        <p>Sonata Music School Production Level</p>
      </header>

      <div className="curriculum-grid">
        {modules.map((item, index) => (
          <div key={index} className="curriculum-card">
            <span className="year-label">{item.year_level}</span>
            <span className="badge-category">{item.category}</span>
            <h3>{item.target_name}</h3>
            <p className="module-text">{item.module_content}</p>
            <div className="teacher-info">
              <div className="teacher-label">Mentor</div>
              <div className="teacher-name">{item.teacher_name}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Curriculum;