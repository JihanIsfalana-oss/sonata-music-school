from flask import Blueprint, request, jsonify
from src.controllers.school_controller import register_student, get_all_students, get_school_info
# PERBAIKAN: Gunakan absolute import jika menjalankan dari root backend
from src.ai_engine import sonata_ai 

api_bp = Blueprint('api', __name__)

api_bp.route('/register', methods=['POST'])(register_student)
api_bp.route('/students', methods=['GET'])(get_all_students)
api_bp.route('/info', methods=['GET'])(get_school_info)

@api_bp.route('/ai/chat', methods=['POST'])
def ai_chat():
    data = request.json
    message = data.get('message')
    # Memanggil fungsi response dari engine Gemini
    response = sonata_ai.get_chatbot_response(message)
    return jsonify({"response": response})

@api_bp.route('/ai/syllabus', methods=['POST'])
def ai_syllabus():
    data = request.json
    # Mengambil data dari form pendaftaran
    name = data.get('name')
    instrument = data.get('instrument')
    genre = data.get('genre')
    
    syllabus = sonata_ai.generate_syllabus(name, instrument, genre)
    return jsonify({"syllabus": syllabus})