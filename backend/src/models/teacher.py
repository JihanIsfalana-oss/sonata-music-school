from .. import db

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False) # Progressive, Rock, etc.
    instrument = db.Column(db.String(50), nullable=False) # Drum, Bass, etc.
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "genre": self.genre,
            "instrument": self.instrument
        }