from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# UserMixin es OBLIGATORIO: Le da a tu usuario los métodos is_authenticated, etc.
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # Función para poner contraseña (la encripta automáticamente)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Función para comprobar contraseña (al hacer login)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)