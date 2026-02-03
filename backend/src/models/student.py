from .. import db  # Titik dua (..) berarti naik satu level ke folder src
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    birth_date = db.Column(db.String(20), nullable=False)
    selected_class = db.Column(db.String(50), nullable=False)
    
    # Menyimpan relasi guru yang terpilih otomatis
    assigned_teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher', backref='students')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "birth_date": self.birth_date,
            "selected_class": self.selected_class,
            "assigned_teacher": self.teacher.name if self.teacher else "Belum ditentukan",
            "joined_date": self.created_at.strftime("%Y-%m-%d")
        }