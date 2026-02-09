import React, { useState, useEffect } from 'react';
import axios from 'axios';

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
    <div className="bg-black min-h-screen p-8 text-white font-sans">
      <header className="mb-12 border-b-2 border-red-600 pb-4">
        <h1 className="text-4xl font-bold uppercase tracking-widest">Mastery Curriculum</h1>
        <p className="text-gray-400">Peta jalan 5 tahun menuju maestro musik profesional.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {modules.map((item, index) => (
          <div key={index} className="bg-zinc-900 border border-zinc-800 p-6 rounded-lg hover:border-red-500 transition-all group">
            <div className="flex justify-between items-start mb-4">
              <span className="bg-red-600 text-xs px-2 py-1 rounded uppercase font-bold">{item.category}</span>
              <span className="text-zinc-500 text-sm">{item.year_level}</span>
            </div>
            <h3 className="text-2xl font-bold mb-2 group-hover:text-red-400">{item.target_name}</h3>
            <p className="text-gray-400 text-sm mb-4 leading-relaxed">
              "{item.module_content}"
            </p>
            <div className="pt-4 border-t border-zinc-800">
              <p className="text-xs text-zinc-500 uppercase tracking-tighter">Mentor</p>
              <p className="text-sm font-medium">{item.teacher_name}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Curriculum;