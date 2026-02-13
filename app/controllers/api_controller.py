from flask import Blueprint, jsonify, request
from app.services.libros_service import *
from app.services.socios_service import *
from app.decorators import role_required

api_bp = Blueprint(
    "api",
    __name__,       
    url_prefix="/api"
)

## Devuelve lista de libros completa en json
@api_bp.route("/libros", methods=["GET"])
def listar():
    libros = listar_libros()
    return jsonify([l.to_dict() for l in libros])   

## Devuelve lista de libros disponibles (sin prestar)
@api_bp.route("/libros/disponibles", methods=["GET"])
def listar_libros_disponibles():
    libros = listar_libros()
    libros_disponibles = [l.to_dict() for l in libros if l.disponible]
    return jsonify(libros_disponibles)

## Devuelve lista de libros que coinciden con la búsqueda
@api_bp.route("/libros/buscar/<string:titulo>", methods=["GET"])
def buscar_libros(titulo):
    libros = listar_libros()
    resultados = [l.to_dict() for l in libros if titulo.lower() in l.titulo.lower()]
    return jsonify(resultados)

## Devuelve la lista de libros prestados
@api_bp.route("/libros/socios/prestamos")
@role_required("admin")
def api_socios_con_prestamos():
    """API: Obtener socios con libros prestados"""
    libros_prestados = listar_libros_prestados()
    resultado = []
    
    for libro in libros_prestados:
        socio = obtener_socio(libro.id_socio)
        if socio:
            resultado.append({
                'socio': socio.to_dict(),
                'libro': libro.to_dict()
            })
    
    return jsonify(resultado)