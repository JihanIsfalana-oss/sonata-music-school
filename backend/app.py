from flask import Flask, jsonify, request
from src import create_app, db
from src.models.student import Student 
from flask_cors import CORS
from dotenv import load_dotenv
from sklearn.neighbors import KNeighborsClassifier
from sqlalchemy import text # Wajib untuk query kurikulum
import numpy as np
import os
import torch
import random
import json

# Import utilitas AI
from ai_engine import SonataChatNet
from nltk_utils import bag_of_words, tokenize

load_dotenv()

app = create_app() 
CORS(app, resources={r"/*": {"origins": "*"}})

# --- SETUP PATHING AMAN UNTUK RAILWAY ---
base_path = os.path.dirname(os.path.abspath(__file__))
intents_path = os.path.join(base_path, 'intents.json')
model_path = os.path.join(base_path, 'models', 'chatbot_model.pth')

# --- SETUP AI CHATBOT (PYTORCH) ---
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open(intents_path, 'r') as f:
    intents = json.load(f)

# Load model dengan proteksi error
try:
    chat_data = torch.load(model_path, map_location=device)
    chat_model = SonataChatNet(chat_data["input_size"], chat_data["hidden_size"], chat_data["output_size"]).to(device)
    chat_model.load_state_dict(chat_data["model_state"])
    chat_model.eval()
    print("--- Model PyTorch Berhasil Dimuat! ---")
except Exception as e:
    print(f"--- Gagal Muat Model: {e} ---")
    chat_data = None

# --- MODEL LAMA (KNN) ---
X_train_vocal = np.array([[3, 8], [4, 9], [2, 7], [8, 4], [9, 5], [7, 3], [5, 5], [6, 6], [5, 4]])
y_train_vocal = ['Rock', 'Rock', 'Rock', 'Opera', 'Opera', 'Opera', 'Pop', 'Pop', 'Pop']
model_vokal = KNeighborsClassifier(n_neighbors=3)
model_vokal.fit(X_train_vocal, y_train_vocal)

# --- FUNGSI SEARCH DATABASE (FITUR KURIKULUM) ---
def get_curriculum_db(msg):
    msg = msg.lower()
    # Mapping input user ke nama kolom target_name di SQL
    targets = {
        'gitar': 'Gitar', 
        'drum': 'Drum', 
        'piano': 'Piano/Keyboard', 
        'keyboard': 'Piano/Keyboard', 
        'bass': 'Bass',
        'rock': 'Rock',
        'pop': 'Pop',
        'blues': 'Blues',
        'progressive': 'Progressive'
    }
    
    # Cari instrumen/genre di dalam pesan
    found_target = next((v for k, v in targets.items() if k in msg), None)
    
    # Perbaikan: Cari angka saja (1-5) agar lebih fleksibel dibanding cari "tahun 1"
    found_year = None
    for i in range(1, 6):
        if str(i) in msg:
            found_year = f"Tahun {i}"
            break

    if found_target and found_year:
        try:
            # Query sesuai tabel curriculum_modules di sonata_db.sql
            query = text("SELECT module_content, teacher_name FROM curriculum_modules WHERE target_name = :t AND year_level = :y")
            result = db.session.execute(query, {"t": found_target, "y": found_year}).fetchone()
            
            if result:
                return f"🎸 Materi {found_target} {found_year}: {result[0]} (Guru: {result[1]})"
        except Exception as e:
            print(f"Error Database: {e}")
            return None
    return None

# --- ROUTES ---
@app.route('/test-chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return jsonify({"status": "Maestro Jihan PyTorch is active!"})
    
    data = request.json
    user_text = data.get("message", "")
    
    if not user_text:
        return jsonify({"reply": "Ketik sesuatu dong, Rocker!"}), 400

    # 1. CEK DATABASE KURIKULUM DULU (Prioritas Utama)
    db_reply = get_curriculum_db(user_text)
    if db_reply:
        return jsonify({"reply": db_reply})

    # 2. JIKA BUKAN TANYA KURIKULUM, GUNAKAN PYTORCH
    if chat_data:
        sentence = tokenize(user_text)
        X = bag_of_words(sentence, chat_data["all_words"])
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = chat_model(X)
        _, predicted = torch.max(output, dim=1)
        tag = chat_data['tags'][predicted.item()]
        
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    return jsonify({"reply": random.choice(intent['responses'])})
    
    return jsonify({"reply": "Waduh, gue belum belajar itu. Coba tanya soal materi Gitar atau Drum Tahun 1-5!"})

@app.route('/curriculum', methods=['GET'])
def get_all_curriculum():
    try:
        # Mengambil semua data modul kurikulum dari SQL
        query = text("SELECT category, target_name, year_level, module_content, teacher_name FROM curriculum_modules")
        results = db.session.execute(query).fetchall()
        
        # Format ke JSON
        curriculum_list = []
        for r in results:
            curriculum_list.append({
                "category": r[0],
                "target_name": r[1],
                "year_level": r[2],
                "module_content": r[3],
                "teacher_name": r[4]
            })
        return jsonify(curriculum_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ... (Route lainnya predict_vocal, delete_student tetap sama) ...