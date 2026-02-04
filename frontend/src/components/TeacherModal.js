import React from 'react';

const TeacherModal = ({ teacher, onClose }) => {
  if (!teacher) return null;

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <button onClick={onClose} style={styles.closeBtn}>&times; Tutup</button>
        
        <h2 style={{ borderBottom: '2px solid #333', paddingBottom: '10px' }}>
          Profil Guru: {teacher.nama}
        </h2>

        <table style={styles.table}>
          <tbody>
            <tr>
              <td style={styles.label}><strong>Riwayat Hidup</strong></td>
              <td>{teacher.riwayat}</td>
            </tr>
            <tr>
              <td style={styles.label}><strong>Kemampuan</strong></td>
              <td>{teacher.kemampuan}</td>
            </tr>
            <tr>
              <td style={styles.label}><strong>Genre</strong></td>
              <td>
                {teacher.genre.map((g, idx) => (
                  <span key={idx} style={styles.tag}>{g}</span>
                ))}
              </td>
            </tr>
            <tr>
              <td style={styles.label}><strong>Referensi Bermusik</strong></td>
              <td>{teacher.referensi}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Styling sederhana (CSS-in-JS) agar tidak perlu buat file CSS terpisah dulu
const styles = {
  overlay: {
    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.7)', display: 'flex', 
    justifyContent: 'center', alignItems: 'center', zIndex: 1000
  },
  modal: {
    backgroundColor: '#fff', padding: '20px', borderRadius: '8px',
    maxWidth: '500px', width: '90%', boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
  },
  closeBtn: {
    float: 'right', border: 'none', background: 'transparent', 
    fontSize: '1.5rem', cursor: 'pointer', color: '#ff4444'
  },
  table: { width: '100%', marginTop: '20px', borderCollapse: 'collapse' },
  label: { width: '30%', padding: '10px', verticalAlign: 'top', color: '#555' },
  tag: { 
    display: 'inline-block', padding: '2px 8px', margin: '2px', 
    borderRadius: '12px', backgroundColor: '#e0e0e0', fontSize: '0.85rem' 
  }
};

export default TeacherModal;