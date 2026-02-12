from app import db
from sqlalchemy import or_
# Importamos cada modelo de SU PROPIA casa
from app.models.socio import Socio
from app.services.libros_service import listar_libros_prestados


def listar_socios():
    return Socio.query.all() 

def obtener_socio(id):
    return Socio.query.get(id)

def listar_socios_con_libros():
    # obtiene lista de libros ya prestados
    libros_prestados = listar_libros_prestados()
    socios_con_libros = set(libro.socio for libro in libros_prestados)
    return list(socios_con_libros)

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

def buscar_socios(termino):
    """
    Busca socios cuyo nombre O email contengan el término.
    Cumple con el requisito R16.
    """
    if not termino:
        return Socio.query.all()
    
    filtro = f"%{termino}%"
    
    # Buscamos coincidencias en nombre O en email (ilike ignora mayúsculas)
    return Socio.query.filter(
        or_(
            Socio.nombre.ilike(filtro),
            Socio.email.ilike(filtro)
        )
    ).all()