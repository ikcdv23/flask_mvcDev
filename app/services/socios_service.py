from app import db
# Importamos cada modelo de SU PROPIA casa
from app.models.socio import Socio
from app.models.libro import Libro


def listar_socios():
    return Socio.query.all() 

def obtener_socio(id):
    return Socio.query.get(id)

def listar_socios_con_libros():
    return Socio.query.join(Libro).all()

def  crear_socio(nombre, email):
    socio = Socio(nombre=nombre, email=email)
    db.session.add(socio)
    db.session.commit()
    return socio    

def editar_socio(socio_id, nombre=None, email=None):
    socio = Socio.query.get(socio_id)
    
    if not socio:
        return None
    if nombre is not None:
        socio.nombre = nombre
    if email is not None:
        socio.email = email
        
    db.session.commit()
    return socio