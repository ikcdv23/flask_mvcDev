from app import db
class Libro(db.Model):
    __tablename__ = "libros"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)  
    autor = db.Column(db.String(100), nullable=False)
    anio = db.Column(db.Integer, nullable=True)
    categoria = db.Column(db.String(100), nullable=True)    
    id_socio = db.Column(db.Integer, db.ForeignKey("socios.id"), nullable=True  )  
    
    # Relación con socio (un libro puede estar prestado a un socio) 
    socio = db.relationship("Socio", back_populates="libros")


    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "anio": self.anio,
            "categoria": self.categoria,
            "id_socio": self.id_socio,
        }
