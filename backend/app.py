from flask import Flask, jsonify, request
from src import create_app, db
from flask_cors import CORS
from sqlalchemy import text
import torch
import torch.nn as nn
import json
import random

# Load data intents untuk respon umum
with open('backend/intents.json', 'r') as f:
    intents_data = json.load(f)

app = create_app() 
CORS(app, resources={r"/*": {"origins": "*"}})

# --- FUNGSI SEARCH DATABASE (KHUSUS KURIKULUM) ---
def search_curriculum(user_message):
    msg = user_message.lower()
    
    # Mapping keyword dari intents.json kamu ke database
    instruments = {
        'gitar': 'Gitar', 'drum': 'Drum', 'bass': 'Bass',
        'piano': 'Piano/Keyboard', 'keyboard': 'Piano/Keyboard',
        'rock': 'Rock', 'pop': 'Pop', 'blues': 'Blues', 'progressive': 'Progressive'
    }
    
    found_target = next((v for k, v in instruments.items() if k in msg), None)
    found_year = next((f"Tahun {i}" for i in range(1, 6) if f"tahun {i}" in msg or f"ke-{i}" in msg), None)

    if found_target and found_year:
        try:
            query = text("SELECT module_content, teacher_name FROM curriculum_modules WHERE target_name = :t AND year_level = :y")
            result = db.session.execute(query, {"t": found_target, "y": found_year}).fetchone()
            if result:
                return f"🎸 **Materi {found_target} ({found_year})**: {result[0]} | **Guru**: {result[1]}"
        except Exception as e:
            return f"Error DB: {str(e)}"
    return None

# --- LOGIKA CHATBOT ---
@app.route('/test-chat', methods=['POST'])
def chat():
    data = request.json
    user_text = data.get("message", "").lower()
    
    # 1. Prioritas: Cek apakah user nanya Kurikulum (Database)
    curriculum_answer = search_curriculum(user_text)
    if curriculum_answer:
        return jsonify({"reply": curriculum_answer})

    # 2. Respon Umum dari intents.json (Simulasi PyTorch Klasifikasi)
    # Nantinya ini diganti dengan model.predict() setelah kamu train
    for intent in intents_data['intents']:
        if 'patterns' in intent: # Pastikan ada patterns (bukan blok curriculum)
            for pattern in intent['patterns']:
                if pattern.lower() in user_text:
                    return jsonify({"reply": random.choice(intent['responses'])})

    # 3. Default Response jika tidak ada yang cocok
    return jsonify({"reply": "Yo Rocker! Gue kurang nangkep maksud lo. Coba tanya soal materi Gitar/Drum atau cara Tes Vokal!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)