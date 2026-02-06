from flask import Flask, jsonify, request
from src import create_app, db
from src.models.student import Student 
from flask_cors import CORS
from dotenv import load_dotenv
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import os
import google.generativeai as genai  

load_dotenv()

app = create_app() 
# Ganti baris CORS lama kamu dengan ini:
CORS(app, resources={r"/*": {
    "origins": [
        "https://sonata-music-school.vercel.app", 
        "http://localhost:3000"
    ],
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# --- SETUP GOOGLE GEMINI (FULL MODE) ---
# Menggunakan API Key yang sudah kamu pasang di Railway (...jUXLU)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Safety settings agar Gemini bebas menjawab soal musik/umum tanpa sensor berlebih
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Ubah bagian inisialisasi model di app.py menjadi:
# Di app.py baris 37, ganti jadi ini saja:
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# --- MODEL KNN (TETAP DIPERTAHANKAN UNTUK PREDIKSI VOKAL) ---
X_train_vocal = np.array([[3, 8], [4, 9], [2, 7], [8, 4], [9, 5], [7, 3], [5, 5], [6, 6], [5, 4]])
y_train_vocal = ['Rock', 'Rock', 'Rock', 'Opera', 'Opera', 'Opera', 'Pop', 'Pop', 'Pop']
model_vokal = KNeighborsClassifier(n_neighbors=3)
model_vokal.fit(X_train_vocal, y_train_vocal)

# --- ROUTES ---
@app.route('/')
def home():
    return jsonify({"message": "Backend Sonata Music School Aktif!", "status": "Ready"})

@app.route('/test-chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return jsonify({"status": "Maestro Jihan Full Gemini Mode Active!"})
    
    data = request.json
    user_text = data.get("message")
    
    if not user_text:
        return jsonify({"reply": "Ketik sesuatu dong, Rocker!"}), 400

    # LANGSUNG TANYA KE GEMINI (TANPA INTENTS.JSON)
    try:
        # Prompt agar Gemini tetap konsisten menjadi persona Maestro Jihan
        prompt_style = (
            f"Kamu adalah Maestro Jihan, asisten musik paling gokil di Sonata Music School. "
            f"Gunakan gaya bahasa anak band yang santai, seru, informatif, dan penuh energi. "
            f"Jawablah pertanyaan user ini dengan cerdas, mau itu soal musik atau pertanyaan umum: {user_text}"
        )
        
        gemini_response = gemini_model.generate_content(prompt_style)
        
        if hasattr(gemini_response, 'text') and gemini_response.text:
            return jsonify({"reply": gemini_response.text})
        else:
            return jsonify({"reply": "Waduh, sinyal studio lagi distorsi nih. Coba tanya lagi, Rocker!"})
            
    except Exception as e:
        print(f"DEBUG_PENTING: {str(e)}") # Ini akan muncul di log Railway
        return jsonify({"reply": f"Error: {str(e)}"}) # Sementara tampilkan errornya di chat

@app.route('/api/predict-vocal', methods=['POST'])
def predict_vocal():
    data = request.json
    prediction = model_vokal.predict([[data.get('pitch'), data.get('power')]])
    return jsonify({
        "recommended_class": prediction[0],
        "message": f"Berdasarkan AI, kamu sangat cocok di kelas {prediction[0]}!"
    })

# --- ROUTE INFO & DATA (DIPERTAHANKAN) ---
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