import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Students.css';

const Students = () => {
  const [students, setStudents] = useState([]);
  const [notification, setNotification] = useState({ show: false, message: '', type: '' });

  const fetchStudents = () => {
    axios.get('https://sonata-music-school-production.up.railway.app/api/students')
      .then(res => setStudents(res.data))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const showToast = (msg, type = 'success') => {
    setNotification({ show: true, message: msg, type: type });
    setTimeout(() => setNotification({ show: false, message: '', type: '' }), 3000);
  };

  const deleteStudent = async (id) => {
    if (window.confirm("Yakin mau hapus musisi ini?")) {
      try {
        await axios.delete(`https://sonata-music-school-production.up.railway.app/api/students/${id}`);
        setStudents(students.filter(s => s.id !== id));
        showToast("Berhasil terhapus! 🗑️", "success");
      } catch (error) {
        showToast("Gagal! Koneksi backstage terputus.", "error");
      }
    }
  };

  const handleEdit = async (student) => {
    const newName = prompt("Ubah Nama Murid:", student.name);
    if (newName) {
      try {
        await axios.put(`https://sonata-music-school-production.up.railway.app/api/students/${student.id}`, {
          ...student,
          name: newName
        });
        showToast("Data murid berhasil diperbarui! 🎤", "success");
        fetchStudents();
      } catch (error) {
        showToast("Gagal update data!", "error");
      }
    }
  };

  return (
    <div className="page">
      <h2>Data Murid Sonata Music School</h2>
      
      {/* ELEMEN NOTIFIKASI KUSTOM */}
      {notification.show && (
        <div className={`toast-notification ${notification.type}`}>
          <div className="toast-content">
            <span className="toast-icon">{notification.type === 'success' ? '🤘' : '⚠️'}</span>
            <span className="toast-message">{notification.message}</span>
          </div>
          <div className="toast-progress"></div>
        </div>
      )}

      <table className="table-custom">
        <thead>
          <tr>
            <th>No</th>
            <th>Nama Murid</th>
            <th>Kelas</th>
            <th>Guru Pengajar</th>
            <th>Umur</th>
            <th>Tgl Lahir</th>
            <th>Aksi</th>
          </tr>
        </thead>
        <tbody>
          {students.map((s, idx) => (
            <tr key={s.id}>
              <td>{idx + 1}</td>
              <td>{s.name}</td>
              <td>{s.selected_class}</td>
              <td>{s.assigned_teacher}</td>
              <td>{s.age}</td>
              <td>{s.birth_date}</td>
              <td>
                <button className="btn-edit" onClick={() => handleEdit(s)}>📝</button>
                <button className="btn-delete" onClick={() => deleteStudent(s.id)}>🗑️</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    
  );
};

export default Students;