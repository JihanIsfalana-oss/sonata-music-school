import React from 'react';

const TeacherModal = ({ teacher, onClose }) => {
  if (!teacher) return null;

  // Data tambahan untuk memperkaya profil
  const extraInfo = {
    riwayat: "Lulusan Seni Musik Universitas dengan pengalaman panggung metal internasional.",
    kemampuan: "Expert di instrumen utama, teori musik, & stage performance.",
    referensi: "Eddie Van Halen, Dream Theater, Jimi Hendrix"
  };

  return (
    <div className="rocker-modal-overlay" onClick={onClose}>
      <div className="rocker-modal-content" onClick={e => e.stopPropagation()}>
        <div className="rocker-modal-header">
          <h2>PROFIL GURU: {teacher.name.toUpperCase()} 🔥🎸</h2>
          <button className="rocker-close-btn" onClick={onClose}>CLOSE</button>
        </div>
        
        <div className="rocker-modal-body">
          <table className="rocker-table">
            <tbody>
              <tr>
                <td><strong>NAMA</strong></td>
                <td className="highlight-text">{teacher.name}</td>
              </tr>
              <tr>
                <td><strong>SPESIALISASI</strong></td>
                <td>{teacher.instrument}</td>
              </tr>
              <tr>
                <td><strong>GENRE UTAMA</strong></td>
                <td>
                  {Array.isArray(teacher.genre) 
                    ? teacher.genre.map((g, i) => <span key={i} className="rocker-tag">{g}</span>)
                    : <span className="rocker-tag">{teacher.genre}</span>}
                </td>
              </tr>
              <tr>
                <td><strong>RIWAYAT</strong></td>
                <td>{extraInfo.riwayat}</td>
              </tr>
              <tr>
                <td><strong>KEMAMPUAN</strong></td>
                <td>{extraInfo.kemampuan}</td>
              </tr>
              <tr>
                <td><strong>REFERENSI MUSIK</strong></td>
                <td className="highlight-text">{extraInfo.referensi}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default TeacherModal;