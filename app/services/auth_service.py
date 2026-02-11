from app import db
from app.models.usuario import Usuario

def verificar_credenciales(username, password):
    """
    Busca al usuario y verifica su contraseña.
    Retorna el objeto Usuario si es correcto, o None si falla.
    """
    # El servicio es quien habla con el Modelo (Usuario.query)
    usuario = Usuario.query.filter_by(username=username).first()
    
    if usuario and usuario.check_password(password):
        return usuario
    
    return None

def crear_usuario_admin(username, password):
    """
    Lógica para crear un usuario en la base de datos.
    """
    # Verificar si ya existe para no duplicar (opcional pero recomendado)
    if Usuario.query.filter_by(username=username).first():
        return False

    nuevo_usuario = Usuario(username=username)
    nuevo_usuario.set_password(password)
    
    db.session.add(nuevo_usuario)
    db.session.commit()
    return True