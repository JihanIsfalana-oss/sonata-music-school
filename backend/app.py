from flask import Flask, jsonify, request
from src import create_app, db
from src.models.student import Student 
from flask_cors import CORS
from dotenv import load_dotenv
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import os
import torch
import random
import json
import google.generativeai as genai  # Tambahan: Library Gemini

# Import utilitas AI yang kita buat di ai_env
from ai_engine import SonataChatNet
from nltk_utils import bag_of_words, tokenize

load_dotenv()

app = create_app() 
CORS(app, resources={r"/*": {"origins": "*"}})

# --- SETUP GOOGLE GEMINI ---
# Mengambil API KEY dari variabel Railway yang sudah kamu masukkan tadi
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# --- SETUP AI CHATBOT (PYTORCH) ---
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load data dan model chatbot
with open('intents.json', 'r') as f:
    intents = json.load(f)

CHAT_MODEL_FILE = "models/chatbot_model.pth"
chat_data = torch.load(CHAT_MODEL_FILE)
chat_model = SonataChatNet(chat_data["input_size"], chat_data["hidden_size"], chat_data["output_size"]).to(device)
chat_model.load_state_dict(chat_data["model_state"])
chat_model.eval()

# --- MODEL LAMA (KNN) TETAP DIPERTAHANKAN ---
X_train_vocal = np.array([[3, 8], [4, 9], [2, 7], [8, 4], [9, 5], [7, 3], [5, 5], [6, 6], [5, 4]])
y_train_vocal = ['Rock', 'Rock', 'Rock', 'Opera', 'Opera', 'Opera', 'Pop', 'Pop', 'Pop']
model_vokal = KNeighborsClassifier(n_neighbors=3)
model_vokal.fit(X_train_vocal, y_train_vocal)

# --- ROUTES ---
@app.route('/')
def home():
    return jsonify({"message": "Backend Sonata Music School Aktif!", "status": "Ready"})

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

# Route Chatbot (Hybrid: PyTorch + Gemini)
@app.route('/test-chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return jsonify({"status": "Chatbot is active! Use POST to talk to me."})
    
    data = request.json
    user_text = data.get("message")
    
    if not user_text:
        return jsonify({"reply": "Ketik sesuatu dong, Rocker!"}), 400

    # 1. Proses dengan PyTorch (Intents Lokal)
    sentence = tokenize(user_text)
    X = bag_of_words(sentence, chat_data["all_words"])
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = chat_model(X)
    _, predicted = torch.max(output, dim=1)
    tag = chat_data['tags'][predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.99 and len(user_text.split()) < 5:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return jsonify({"reply": random.choice(intent['responses'])})
    
    # PAKSA TANYA GEMINI
    try:
        prompt_style = f"Kamu adalah Maestro Jihan. Jawab santai & rocker: {user_text}"
        gemini_response = gemini_model.generate_content(prompt_style)
        return jsonify({"reply": gemini_response.text})
    except Exception as e:
        return jsonify({"reply": "Gue lagi tuning gitar, tanya soal kelas aja dulu!"})
    
@app.route('/api/predict-vocal', methods=['POST'])
def predict_vocal():
    data = request.json
    pitch = data.get('pitch')
    power = data.get('power')
    prediction = model_vokal.predict([[pitch, power]])
    return jsonify({
        "recommended_class": prediction[0],
        "message": f"Berdasarkan AI, kamu sangat cocok di kelas {prediction[0]}!"
    })

@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        student = db.session.get(Student, id) 
        if student:
            db.session.delete(student)
            db.session.commit()
            return jsonify({"message": "Data berhasil dihapus"}), 200
        return jsonify({"error": "Data tidak ditemukan"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    try:
        student = db.session.get(Student, id)
        data = request.json
        if student:
            student.name = data.get('name', student.name)
            db.session.commit()
            return jsonify({"message": "Data berhasil diupdate"}), 200
        return jsonify({"error": "Data tidak ditemukan"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

print("\n--- DAFTAR ALAMAT API KAMU ---")
for rule in app.url_map.iter_rules():
    print(f"Alamat: {rule.rule} --> Fungsi: {rule.endpoint}")
print("------------------------------\n")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)