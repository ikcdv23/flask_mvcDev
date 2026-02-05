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

def editar_socio(id, nuevo_nombre, nuevo_email):
    socio = obtener_socio(id)
    if socio:
        socio.nombre = nuevo_nombre
        socio.email = nuevo_email
        db.session.commit()
        return True
    return False

def borrar_socio(socio_id):
    socio = Socio.query.get(socio_id)
    if socio:
        # R15: Verificamos si tiene libros prestados
        if len(socio.libros) > 0:
            return False, "No se puede borrar: el socio tiene libros pendientes."
        
        db.session.delete(socio)
        db.session.commit()
        return True, "Socio eliminado con éxito."
    return False, "Socio no encontrado."