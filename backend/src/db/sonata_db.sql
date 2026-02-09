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

CREATE TABLE curriculum_modules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category ENUM('Instrument', 'Genre') NOT NULL,
    target_name VARCHAR(50) NOT NULL, -- Nama Alat atau Nama Genre
    year_level VARCHAR(20) NOT NULL,  -- Tahun 1 sampai Tahun 5
    module_content TEXT NOT NULL,
    teacher_name VARCHAR(150)
);

-- MODUL INSTRUMEN
INSERT INTO curriculum_modules (category, target_name, year_level, module_content, teacher_name) VALUES 
('Instrument', 'Gitar', 'Tahun 1', 'Dasar fingering, tangga nada mayor, dan teknik strumming dasar.', 'Ernest, S.T., M.Sn'),
('Instrument', 'Gitar', 'Tahun 2', 'Teknik legato, vibrato, dan speed picking tahap awal.', 'Ernest, S.T., M.Sn'),
('Instrument', 'Gitar', 'Tahun 3', 'Sweep picking, tapping, dan eksplorasi efek pedal.', 'Ernest, S.T., M.Sn'),
('Instrument', 'Gitar', 'Tahun 4', 'Aransemen solo gitar dan teknik improvisasi modal.', 'Ernest, S.T., M.Sn'),
('Instrument', 'Gitar', 'Tahun 5', 'Penguasaan fretboard total dan penciptaan karakter suara unik.', 'Ernest, S.T., M.Sn'),

('Instrument', 'Drum', 'Tahun 1', 'Rudiments dasar (single/double stroke) dan koordinasi tangan-kaki.', 'Dr.Ir.Falan, Ph.D'),
('Instrument', 'Drum', 'Tahun 2', 'Dinamika hi-hat, penggunaan crash/ride, dan double pedal dasar.', 'Dr.Ir.Falan, Ph.D'),
('Instrument', 'Drum', 'Tahun 3', 'Teknik blast beat, linear drumming, dan kontrol tempo tinggi.', 'Dr.Ir.Falan, Ph.D'),
('Instrument', 'Drum', 'Tahun 4', 'Eksplorasi sound drum dan teknik rekaman perkusi.', 'Dr.Ir.Falan, Ph.D'),
('Instrument', 'Drum', 'Tahun 5', 'Solo drum eksperimental dan penguasaan poliritmik kompleks.', 'Dr.Ir.Falan, Ph.D'),

('Instrument', 'Piano/Keyboard', 'Tahun 1', 'Postur tangan, membaca not balok, dan tangga nada diatonis.', 'Yurika, S.Ikom'),
('Instrument', 'Piano/Keyboard', 'Tahun 2', 'Arpeggio, chord inversions, dan penggunaan teknik pedal.', 'Yurika, S.Ikom'),
('Instrument', 'Piano/Keyboard', 'Tahun 3', 'Synthesizer sound design dan comping gaya modern.', 'Yurika, S.Ikom'),
('Instrument', 'Piano/Keyboard', 'Tahun 4', 'Harmoni jazz-pop dan teknik improvisasi melodi.', 'Yurika, S.Ikom'),
('Instrument', 'Piano/Keyboard', 'Tahun 5', 'Komposisi piano klasik-kontemporer dan manajemen MIDI.', 'Yurika, S.Ikom'),

('Instrument', 'Bass', 'Tahun 1', 'Teknik plucking dua jari dan menjaga tempo pada root note.', 'Ir. Arraya Bey, S.Pd'),
('Instrument', 'Bass', 'Tahun 2', 'Walking bass lines dasar dan teknik hammer-on/pull-off.', 'Ir. Arraya Bey, S.Pd'),
('Instrument', 'Bass', 'Tahun 3', 'Teknik slapping dasar dan sinkopasi kompleks.', 'Ir. Arraya Bey, S.Pd'),
('Instrument', 'Bass', 'Tahun 4', 'Fretboard mastery dan teknik bass solo.', 'Ir. Arraya Bey, S.Pd'),
('Instrument', 'Bass', 'Tahun 5', 'Advanced slapping, tapping bass, dan sinkronisasi drum-bass.', 'Ir. Arraya Bey, S.Pd');

-- MODUL GENRE
INSERT INTO curriculum_modules (category, target_name, year_level, module_content, teacher_name) VALUES 
('Genre', 'Pop', 'Tahun 1', 'Memahami struktur lagu Pop modern dan ear training dasar.', 'Yurika, S.Ikom'),
('Genre', 'Pop', 'Tahun 2', 'Groove pop, sinkopasi, dan dinamika emosi lagu.', 'Yurika, S.Ikom'),
('Genre', 'Pop', 'Tahun 3', 'Teknik aransemen backing vocal dan elemen digital.', 'Yurika, S.Ikom'),
('Genre', 'Pop', 'Tahun 4', 'Songwriting mastery (hook writing) dan produksi DAW.', 'Yurika, S.Ikom'),
('Genre', 'Pop', 'Tahun 5', 'Branding musisi Pop dan persiapan rilis single.', 'Yurika, S.Ikom'),

('Genre', 'Progressive', 'Tahun 1', 'Dasar-dasar ketukan ganjil (odd meters).', 'Dr.Ir.Falan, Ph.D'),
('Genre', 'Progressive', 'Tahun 2', 'Struktur lagu panjang (epics) dan perubahan tempo mendadak.', 'Dr.Ir.Falan, Ph.D'),
('Genre', 'Progressive', 'Tahun 3', 'Odd time signatures kompleks dan sinkopasi berat.', 'Dr.Ir.Falan, Ph.D'),
('Genre', 'Progressive', 'Tahun 4', 'Teori musik tingkat lanjut untuk komposisi progresif.', 'Dr.Ir.Falan, Ph.D'),
('Genre', 'Progressive', 'Tahun 5', 'Pembuatan album konsep progresif profesional.', 'Dr.Ir.Falan, Ph.D'),

('Genre', 'Rock', 'Tahun 1', 'Struktur lagu Rock (Verse-Chorus) dan energi panggung.', 'Ir. Arraya Bey, S.Pd'),
('Genre', 'Rock', 'Tahun 2', 'Penggunaan distorsi dan sejarah Rock n Roll.', 'Ir. Arraya Bey, S.Pd'),
('Genre', 'Rock', 'Tahun 3', 'Eksplorasi sub-genre (Punk, Metal) dan penulisan lirik.', 'Ir. Arraya Bey, S.Pd'),
('Genre', 'Rock', 'Tahun 4', 'Produksi musik Rock studio dan live band performance.', 'Ir. Arraya Bey, S.Pd'),
('Genre', 'Rock', 'Tahun 5', 'Menemukan identitas musik Rock orisinal.', 'Ir. Arraya Bey, S.Pd'),

('Genre', 'Blues', 'Tahun 1', 'Sejarah Blues dan struktur dasar 12-bar blues.', 'Ernest, S.T., M.Sn'),
('Genre', 'Blues', 'Tahun 2', 'Teknik call and response dalam permainan musik.', 'Ernest, S.T., M.Sn'),
('Genre', 'Blues', 'Tahun 3', 'Tangga nada Blues dan modulasi antar nada.', 'Ernest, S.T., M.Sn'),
('Genre', 'Blues', 'Tahun 4', 'Improvisasi emosional dan dinamika soul dalam musik.', 'Ernest, S.T., M.Sn'),
('Genre', 'Blues', 'Tahun 5', 'Eksplorasi Blues modern dan crossover genre.', 'Ernest, S.T., M.Sn');

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