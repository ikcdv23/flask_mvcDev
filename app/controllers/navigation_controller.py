from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.forms.libro_form import LibroForm
from app.models import libro
from app.models.libro import Libro
from app.services import libros_service
from app.services.libros_service import crear_libro, editar_libro, listar_libros
from flask_login import current_user

navigation_bp = Blueprint(
    "navigation",
    __name__,
    url_prefix="/"
)

@navigation_bp.route("/")
def inicio():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template("paginas/inicio.html")

