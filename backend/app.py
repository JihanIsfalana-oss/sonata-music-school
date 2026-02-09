from flask import Flask, jsonify, request
from src import create_app, db
from src.models.student import Student 
from flask_cors import CORS
from dotenv import load_dotenv
from sklearn.neighbors import KNeighborsClassifier
from sqlalchemy import text  # Tambahkan ini untuk eksekusi SQL manual
import numpy as np
import os
import google.generativeai as genai  

load_dotenv()

app = create_app() 

CORS(app, resources={r"/*": {
    "origins": [
        "https://sonata-music-school.vercel.app", 
        "http://localhost:3000"
    ],
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# --- SETUP GOOGLE GEMINI ---
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- MODEL KNN UNTUK VOKAL ---
X_train_vocal = np.array([[3, 8], [4, 9], [2, 7], [8, 4], [9, 5], [7, 3], [5, 5], [6, 6], [5, 4]])
y_train_vocal = ['Rock', 'Rock', 'Rock', 'Opera', 'Opera', 'Opera', 'Pop', 'Pop', 'Pop']
model_vokal = KNeighborsClassifier(n_neighbors=3)
model_vokal.fit(X_train_vocal, y_train_vocal)

# --- FUNGSI OTOMATIS AMBIL KURIKULUM DARI DB ---
def get_curriculum_from_db(user_message):
    """Mencari materi di tabel curriculum_modules berdasarkan keyword user"""
    msg = user_message.lower()
    
    # List target yang ada di database kamu
    targets = ['gitar', 'drum', 'piano', 'keyboard', 'bass', 'rock', 'pop', 'blues', 'progressive']
    years = ['tahun 1', 'tahun 2', 'tahun 3', 'tahun 4', 'tahun 5']
    
    found_target = next((t for t in targets if t in msg), None)
    found_year = next((y for y in years if y in msg), None)

    if found_target and found_year:
        try:
            # Query ke tabel yang kamu buat tadi
            # Menggunakan mapping untuk Piano/Keyboard agar cocok dengan DB
            search_target = "Piano/Keyboard" if found_target in ['piano', 'keyboard'] else found_target.capitalize()
            
            query = text("SELECT module_content, teacher_name FROM curriculum_modules WHERE target_name = :target AND year_level = :year")
            result = db.session.execute(query, {"target": search_target, "year": found_year.capitalize()}).fetchone()
            
            if result:
                return f"Materi {search_target} {found_year}: {result[0]} (Guru: {result[1]})"
        except Exception as e:
            print(f"DB_ERROR: {str(e)}")
    return None

# --- ROUTES ---
@app.route('/')
def home():
    return jsonify({"message": "Backend Sonata Music School Aktif!", "status": "Ready"})

@app.route('/test-chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return jsonify({"status": "Maestro Jihan Full Gemini Mode Active!"})
    
    data = request.json
    user_text = data.get("message", "")
    
    if not user_text:
        return jsonify({"reply": "Ketik sesuatu dong, Rocker!"}), 400

    # 1. CEK DATABASE DULU
    curriculum_info = get_curriculum_from_db(user_text)

    # 2. TANYA GEMINI DENGAN CONTEXT DARI DATABASE
    try:
        # Masukkan info kurikulum ke prompt agar Gemini tahu isinya
        db_context = f"\nINFO DARI DATABASE KURIKULUM: {curriculum_info}" if curriculum_info else ""
        
        prompt_style = (
            f"Kamu adalah Maestro Jihan, asisten musik paling gokil di Sonata Music School. "
            f"Gunakan gaya bahasa anak band yang santai, seru, informatif, dan penuh energi. "
            f"{db_context}\n"
            f"User bertanya: {user_text}\n"
            f"Jawablah dengan cerdas. Jika ada info dari database, gunakan info tersebut!"
        )
        
        gemini_response = gemini_model.generate_content(prompt_style)
        
        if hasattr(gemini_response, 'text') and gemini_response.text:
            return jsonify({"reply": gemini_response.text})
        else:
            return jsonify({"reply": "Waduh, sinyal studio lagi distorsi nih. Coba tanya lagi!"})
            
    except Exception as e:
        print(f"DEBUG_PENTING: {str(e)}")
        return jsonify({"reply": f"Error: {str(e)}"})

@app.route('/api/predict-vocal', methods=['POST'])
def predict_vocal():
    data = request.json
    prediction = model_vokal.predict([[data.get('pitch'), data.get('power')]])
    return jsonify({
        "recommended_class": prediction[0],
        "message": f"Berdasarkan AI, kamu sangat cocok di kelas {prediction[0]}!"
    })

@app.route('/api/info', methods=['POST'])
def get_info():
    return jsonify({
        "vision": "Menjadi sekolah musik pilihan utama yang menghasilkan maestro berbakat.",
        "contact": "Jl. Musik No. 123, Jakarta",
        "teachers": [
            {"id": 1, "name": "Maestro Jihan", "genre": "Rock", "instrument": "Electric Guitar"},
            {"id": 2, "name": "Prof. Isfalana", "genre": "Pop", "instrument": "Piano"}
        ]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)