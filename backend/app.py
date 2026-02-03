from flask import Flask, jsonify, request
from src import create_app, db
# Menyesuaikan dengan struktur folder kamu:
from src.models.student import Student 
from flask_cors import CORS
from dotenv import load_dotenv
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

load_dotenv()

# Gunakan create_app() saja, hapus baris app = Flask(__name__)
app = Flask(__name__)
# Izinkan semua origin agar lebih mudah saat testing
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- FUNGSI HAPUS MURID ---
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        # Cara ini lebih stabil untuk Flask-SQLAlchemy terbaru
        student = db.session.get(Student, id) 
        
        if student:
            db.session.delete(student)
            db.session.commit()
            return jsonify({"message": "Data berhasil dihapus"}), 200
        return jsonify({"error": "Data tidak ditemukan"}), 404
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}") # Cek pesan ini di terminal VS Code jika masih gagal
        return jsonify({"error": str(e)}), 500

# --- ROUTE UNTUK EDIT ---
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    try:
        student = db.session.get(Student, id)
        data = request.json
        if student:
            # Update nama
            student.name = data.get('name', student.name)
            # Kamu bisa tambah field lain di sini, contoh:
            # student.age = data.get('age', student.age)
            
            db.session.commit()
            return jsonify({"message": "Data berhasil diupdate"}), 200
        return jsonify({"error": "Data tidak ditemukan"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
X_train = np.array([[3, 8], [4, 9], [2, 7],   # Karakter Rock
                    [8, 4], [9, 5], [7, 3],   # Karakter Opera
                    [5, 5], [6, 6], [5, 4]])  # Karakter Pop
y_train = ['Rock', 'Rock', 'Rock', 'Opera', 'Opera', 'Opera', 'Pop', 'Pop', 'Pop']

# Inisialisasi Model
model_vokal = KNeighborsClassifier(n_neighbors=3)
model_vokal.fit(X_train, y_train)

@app.route('/api/predict-vocal', methods=['POST'])
def predict_vocal():
    data = request.json
    pitch = data.get('pitch')
    power = data.get('power')
    
    # Prediksi
    prediction = model_vokal.predict([[pitch, power]])
    return jsonify({
        "recommended_class": prediction[0],
        "message": f"Berdasarkan AI, kamu sangat cocok di kelas {prediction[0]}!"
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)