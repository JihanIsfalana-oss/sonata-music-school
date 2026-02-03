import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    birth_date: '',
    selected_class: 'Progressive' // Default option
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/register', formData);
      alert('Pendaftaran Berhasil! Guru telah ditentukan otomatis.');
      navigate('/students');
    } catch (error) {
      alert('Gagal mendaftar: ' + error.response?.data?.message);
    }
  };

  return (
    <div className="page">
      <h2>Formulir Pendaftaran Murid Baru</h2>
      <form onSubmit={handleSubmit} className="form-box">
        <label>Nama Lengkap:</label>
        <input type="text" name="name" onChange={handleChange} required />

        <label>Umur:</label>
        <input type="number" name="age" onChange={handleChange} required />

        <label>Tanggal Lahir:</label>
        <input type="date" name="birth_date" onChange={handleChange} required />

        <label>Pilih Kelas:</label>
        <select name="selected_class" onChange={handleChange}>
          <option value="Progressive">Progressive</option>
          <option value="Rock">Rock</option>
          <option value="Pop">Pop</option>
          <option value="Blues">Blues</option>
        </select>

        <button type="submit">Daftar Sekarang</button>
      </form>
    </div>
  );
};

export default Register;