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
import google.generativeai as genai  

# Import utilitas AI yang kita buat di ai_env
from ai_engine import SonataChatNet
from nltk_utils import bag_of_words, tokenize

load_dotenv()

app = create_app() 
CORS(app, resources={r"/*": {"origins": "*"}})

# --- SETUP GOOGLE GEMINI (VERSI ANTI-PANIK) ---
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Menambahkan Safety Settings agar Gemini tidak memblokir pertanyaan musik/masak
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

gemini_model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    safety_settings=safety_settings
)

# --- SETUP AI CHATBOT (PYTORCH) ---
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as f:
    intents = json.load(f)

CHAT_MODEL_FILE = "models/chatbot_model.pth"
chat_data = torch.load(CHAT_MODEL_FILE)
chat_model = SonataChatNet(chat_data["input_size"], chat_data["hidden_size"], chat_data["output_size"]).to(device)
chat_model.load_state_dict(chat_data["model_state"])
chat_model.eval()

# --- MODEL KNN (TETAP SAMA) ---
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

@app.route('/test-chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return jsonify({"status": "Chatbot is active! Use POST to talk to me."})
    
    data = request.json
    user_text = data.get("message")
    
    if not user_text:
        return jsonify({"reply": "Ketik sesuatu dong, Rocker!"}), 400

    # 1. Proses dengan PyTorch
    sentence = tokenize(user_text)
    X = bag_of_words(sentence, chat_data["all_words"])
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = chat_model(X)
    _, predicted = torch.max(output, dim=1)
    tag = chat_data['tags'][predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    # Logika Threshold Super Ketat (0.99)
    if prob.item() > 0.99 and len(user_text.split()) < 5:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return jsonify({"reply": random.choice(intent['responses'])})
    
    # 2. PAKSA TANYA GEMINI (DENGAN PENANGANAN ERROR)
    try:
        prompt_style = f"Kamu adalah Maestro Jihan, asisten musik paling gokil. Jawab santai dan rocker: {user_text}"
        gemini_response = gemini_model.generate_content(prompt_style)
        
        # Pastikan ada teks di responnya
        if hasattr(gemini_response, 'text') and gemini_response.text:
            return jsonify({"reply": gemini_response.text})
        else:
            return jsonify({"reply": "Waduh, otak gue lagi distorsi. Bisa tanya yang lain?"})
            
    except Exception as e:
        print(f"ERROR GEMINI: {str(e)}") # Muncul di Deploy Logs Railway
        return jsonify({"reply": "Sinyal studio lagi pecah, Rocker! Coba cek API Key atau tanya soal sekolah aja."})

@app.route('/api/predict-vocal', methods=['POST'])
def predict_vocal():
    data = request.json
    prediction = model_vokal.predict([[data.get('pitch'), data.get('power')]])
    return jsonify({"recommended_class": prediction[0]})

# ... (Route DELETE dan PUT tetap sama) ...

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)