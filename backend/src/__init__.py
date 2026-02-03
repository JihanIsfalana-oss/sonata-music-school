from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    # PENTING: Import model DI SINI agar SQLAlchemy mengenali adanya tabel
    from .models.teacher import Teacher
    from .models.student import Student
    
    from .routes.api_routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    with app.app_context():
        # Membuat tabel jika belum ada
        db.create_all()
        
        # Seeding data Guru (Sama seperti logika C++ Anda)
        if not Teacher.query.first():
            print("--- Mengisi Data Guru Awal ---")
            teachers_data = [
                Teacher(genre="Progressive", name="Dr.Ir.Falan, S.Kom.,M.M.,Ph.D", instrument="Drum"),
                Teacher(genre="Pop", name="Yurika, S.Ikom", instrument="Keyboard/Piano"),
                Teacher(genre="Blues", name="Ernest, S.T., M.Sn", instrument="Gitar"),
                Teacher(genre="Rock", name="Ir. Arraya Bey, S.Pd", instrument="Bass")
            ]
            db.session.add_all(teachers_data)
            db.session.commit()
            print("--- Data Guru Berhasil Masuk ---")
            
    return app