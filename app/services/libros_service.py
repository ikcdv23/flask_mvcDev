from app.models import libro
from sqlalchemy import func
from app import db
from app.models.libro import Libro


### Servicios para listar libros ###     
def listar_libros():
    return Libro.query.all()
    #return Libro.query.order_by(func.lower(Libro.titulo)).all()

def listar_libros_disponibles():
    return Libro.query.filter(Libro.codigo_socio == None).all()

def listar_libros_prestados():
    return Libro.query.filter(Libro.codigo_socio != None).all()

def obtener_libro(id):
    return Libro.query.get(id)

def buscar_libros_por_titulo(titulo):
    return Libro.query.filter(Libro.titulo.ilike(f"%{titulo}%")).all()


#### Funciones para crear y editar libros ###   
def crear_libro(titulo, autor, anio=None, categoria=None, id_socio=None):
    libro = Libro(titulo=titulo, autor=autor, anio=anio, categoria=categoria, id_socio=id_socio)
    db.session.add(libro)
    db.session.commit()
    return libro

def editar_libro(libro_id, titulo=None, autor=None, anio=None, categoria=None, id_socio=None):
    libro = Libro.query.get(libro_id)
    
    if not libro:
        return None
    if titulo is not None:
        libro.titulo = titulo
    if autor is not None:
        libro.autor = autor
    if anio is not None:
        libro.anio = anio
    if categoria is not None:
        libro.categoria = categoria
    if id_socio is not None:
        libro.id_socio = id_socio
        
    db.session.commit()
    return libro

#### funciones para gestionar prestamos ####   
def prestar_libro(libro_id, id_socio):
    libro = Libro.query.get(libro_id)

    if libro and libro.id_socio is None:
        
        libro.id_socio =  id_socio
        db.session.commit()
        return libro
    
    return None

### Devolver el libro
def devolver_libro(id_libro):
    # 1. Buscamos el libro
    libro = Libro.query.get(id_libro)
    
    # 2. Si el libro existe, ponemos el socio a None (Vacío)
    if libro:
        # ¡OJO! Asegúrate que en tu modelo 'Libro' el campo se llama 'id_socio'
        libro.id_socio = None 
        db.session.commit()
        return True
    return False