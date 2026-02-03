import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Menggunakan SQLite agar langsung jalan tanpa setup ribet. 
    # Ganti string ini jika nanti ingin pakai MySQL.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, '../../sonata.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False