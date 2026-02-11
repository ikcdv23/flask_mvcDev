
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
# para manejar sesiones de usuario
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager() ## sale de flask login

def create_app():

    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = 'root' # Necesario para sesiones
    ###
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///python.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # evitar warning de SQLAlchemy
     # 🔐 CLAVE SECRETA (obligatoria para Flask-WTF)
    app.config["SECRET_KEY"] = "dev-secret-key"  # luego la convendría cambiarla por una más segura en producción

    db.init_app(app)

    ### Configuración del Login Manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # A dónde te manda si no estás logueado
    ####
    
    # Registro de los Blueprints
    
    from app.controllers.auth_controller import auth_bp ### controlador de autenticacion de sesion
    app.register_blueprint(auth_bp)
    
    from app.controllers.navigation_controller import navigation_bp
    app.register_blueprint(navigation_bp)
    
    from app.controllers.libros_controller import libros_bp
    app.register_blueprint(libros_bp)
    
    from app.controllers.socios_controller import socios_bp
    app.register_blueprint(socios_bp)
    
    from app.controllers.api_controller import api_bp
    app.register_blueprint(api_bp)

        # Crear las tablas en la base de datos
    with app.app_context():
        from app.models.socio import Socio
        from app.models.libro import Libro
        db.create_all()

    return app

# Esto sirve para que Flask sepa buscar al usuario en la BD por su ID ### NUEVO
@login_manager.user_loader
def load_user(id):
    from app.models.usuario import Usuario
    return Usuario.query.get(int(id))