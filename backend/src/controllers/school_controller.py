from flask import jsonify, request
# Mengambil db dari folder induk (src)
from .. import db 
# Mengambil models dari folder tetangga
from ..models.student import Student
from ..models.teacher import Teacher

# 1. Logic untuk Pendaftaran (Register)
def register_student():
    data = request.json
    
    # Cari guru berdasarkan genre kelas (Logika map relasiGuru di C++)
    teacher = Teacher.query.filter_by(genre=data['selected_class']).first()
    
    if not teacher:
        return jsonify({"status": "error", "message": "Maaf, belum ada guru untuk kelas tersebut"}), 404
        
    new_student = Student(
        name=data['name'],
        age=data['age'],
        birth_date=data['birth_date'],
        selected_class=data['selected_class'],
        assigned_teacher_id=teacher.id
    )
    
    try:
        db.session.add(new_student)
        db.session.commit()
        return jsonify({
            "status": "success", 
            "message": "Pendaftaran Berhasil!",
            "data": new_student.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# 2. Logic Lihat Murid
def get_all_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])

# 3. Logic Lihat Guru & Info Sekolah
def get_school_info():
    teachers = Teacher.query.all()
    info = {
        "school_name": "Sonata Music School",
        "vision": "Menjadi pusat pendidikan musik terdepan berbasis teknologi & seni.",
        "contact": "Jl. Pesanggrahan No. 88, Jakarta Selatan",
        "teachers": [t.to_dict() for t in teachers]
    }
    return jsonify(info)