from app import db

class Socio(db.Model):  
    __tablename__ = "socios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)            

    # Relación con libros (un socio puede tener varios libros prestados)
    libros = db.relationship("Libro", back_populates="socio")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "libros": [l.id for l in self.libros]    
        }