# 🎵 Sonata Music School System

**Sonata Music School System** adalah aplikasi manajemen sekolah musik berbasis CLI (Command Line Interface) yang dibuat menggunakan bahasa C++. Program ini dirancang untuk mempermudah proses pendaftaran siswa baru dan pengelolaan data dasar sekolah.

## 📋 Fitur Utama

### 1. Pendaftaran Murid Baru 📝
Fitur ini memungkinkan pengguna untuk mendaftarkan siswa dengan atribut lengkap:
* **Biodata:** Nama, Umur, Tanggal Lahir.
* **Pilihan Kelas Genre:**
    1. Progressive
    2. Rock
    3. Pop
    4. Blues
* **Pilihan Peminatan Alat Musik:**
    1. Gitar
    2. Drum
    3. Bass
    4. Keyboard/Piano

> **Catatan:** Data siswa yang berhasil didaftarkan akan otomatis disimpan (append) ke dalam file eksternal bernama `Data murid baru.txt`.

### 2. Manajemen Guru (Back-End) 👨‍🏫
Sistem memiliki struktur data (`Class Guru`) untuk menyimpan data pengajar, termasuk fitur enkapsulasi untuk pengelolaan gaji guru.

### 3. Informasi Sekolah ℹ️
Menu navigasi tersedia untuk melihat riwayat guru dan informasi tentang sekolah (Fitur dalam tahap pengembangan/modul terpisah).

## 🛠️ Struktur Kode & Teknologi

Program ini dibangun menggunakan konsep **Object-Oriented Programming (OOP)**:

* **Language:** C++
* **Class `Daftar`:** Menangani atribut siswa dan array untuk opsi kelas/alat musik.
* **Class `Guru`:** Menangani atribut pengajar dengan *access modifier* private untuk keamanan data gaji.
* **File Handling:** Menggunakan library `<fstream>` untuk menyimpan output pendaftaran secara permanen.

## 🚀 Cara Menjalankan

1.  **Compile Program:**
    Pastikan Anda memiliki compiler C++ (seperti g++).
    ```bash
    g++ SONATA.cpp -o sonata
    ```

2.  **Run Program:**
    ```bash
    sonata.exe
    ```

## 📄 Format Output Data
Data akan tersimpan di `Data murid baru.txt` dengan format rapi seperti berikut:

```text
           ======== Data Murid Baru ========           
Nama                 : [Nama Siswa]|
Kelas                : [Genre]|
Alat Musik           : [Instrumen]|
Umur                 : [Angka]|
Tanggal Lahir        : [Tanggal]|
