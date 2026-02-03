CREATE DATABASE sonata_music_school;
USE sonata_music_school;

-- 1. Tabel Informasi Sekolah (Pengganti fungsi Tentang_Kami)
CREATE TABLE school_profile (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    vision TEXT,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    opening_hours VARCHAR(100)
);

-- 2. Tabel Misi Sekolah (Relasi One-to-Many dari Profile)
CREATE TABLE school_missions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    profile_id INT,
    mission_text TEXT,
    FOREIGN KEY (profile_id) REFERENCES school_profile(id)
);

-- 3. Tabel Kategori Instrumen (Spesialisasi Alat)
CREATE TABLE instruments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    instrument_name VARCHAR(50) NOT NULL -- Gitar, Drum, Bass, Piano
);

-- 4. Tabel Genre/Kelas (Kategori Kelas)
CREATE TABLE genres (
    id INT PRIMARY KEY AUTO_INCREMENT,
    genre_name VARCHAR(50) NOT NULL -- Progressive, Rock, Pop, Blues
);

-- 5. Tabel Guru (Pengganti class Guru)
CREATE TABLE teachers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(150) NOT NULL,
    specialty_id INT,
    base_salary DECIMAL(15, 2), -- Dari listGaji di C++
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (specialty_id) REFERENCES instruments(id)
);

-- 6. Tabel Relasi Guru dan Genre (Siapa mengajar kelas apa)
CREATE TABLE teacher_genre_assignments (
    teacher_id INT,
    genre_id INT,
    PRIMARY KEY (teacher_id, genre_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id)
);

-- 7. Tabel Murid (Pengganti class Daftar)
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(150) NOT NULL,
    age INT,
    birth_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Tabel Pendaftaran (Transaksi antara Murid, Guru, dan Kelas)
CREATE TABLE enrollments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    teacher_id INT,
    genre_id INT,
    registration_date DATE,
    status ENUM('Active', 'Graduated', 'Dropped'),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id)
);
-- Input Instrumen & Genre
INSERT INTO instruments (instrument_name) VALUES ('Drum'), ('Keyboard/Piano'), ('Gitar'), ('Bass');
INSERT INTO genres (genre_name) VALUES ('Progressive'), ('Pop'), ('Blues'), ('Rock');

-- Input Guru & Gaji (Sesuai listGaji dan spesialisAlat di C++)
INSERT INTO teachers (full_name, specialty_id, base_salary) VALUES 
('Dr.Ir.Falan, S.Kom.,M.M.,Ph.D', 1, 3500000),
('Yurika, S.Ikom', 2, 1250000),
('Ernest, S.T., M.Sn', 3, 5000000),
('Ir. Arraya Bey, S.Pd', 4, 2300000);

-- Input Relasi Guru & Genre (Sesuai relasiGuru di C++)
INSERT INTO teacher_genre_assignments (teacher_id, genre_id) VALUES 
(1, 1), -- Falan di Progressive
(2, 2), -- Yurika di Pop
(3, 3), -- Ernest di Blues
(4, 4); -- Arraya di Rock
SELECT 
    s.full_name AS Murid, 
    g.genre_name AS Kelas, 
    t.full_name AS Guru,
    i.instrument_name AS Alat
FROM enrollments e
JOIN students s ON e.student_id = s.id
JOIN teachers t ON e.teacher_id = t.id
JOIN genres g ON e.genre_id = g.id
JOIN instruments i ON t.specialty_id = i.id;