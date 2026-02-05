from flask import Blueprint, render_template, request, redirect, url_for
from app.forms.socio_form import SocioForm
from app.models.socio import Socio
from app.services.socios_service import *

socios_bp = Blueprint(
    "socios",       
    __name__,
    url_prefix="/socios"
)

@socios_bp.route("/")
def listar():
    socios = listar_socios()
    return render_template("paginas/socios/socios.html", socios=socios)

@socios_bp.route("/con-prestamos")
def listar_con_prestamos():
    # Usamos la función especial que creaste en el servicio
    socios = listar_socios_con_libros()
    return render_template("paginas/socios/socios_prestamos.html", socios=socios)

## Ruta para crear un socio 
@socios_bp.route("/crear", methods=["GET", "POST"])
def crear():   
    form = SocioForm()  
    if request.method == "POST":
        if form.validate_on_submit():
            nombre = form.nombre.data
            email = form.email.data           

            crear_socio(nombre, email)         

            return redirect(url_for("socios.listar"))  
    return render_template("paginas/socios/socio_crear.html", form=form)     

## Ruta para erditar el socio 
@socios_bp.route("/editar/<int:id>", methods=["GET", "POST"])   
def editar(id):
    socio = obtener_socio(id)
    
    if not socio:
        return "Socio no encontrado", 404

    form = SocioForm(obj=socio)

    if form.validate_on_submit():
        editar_socio(
            socio_id=id,
            nombre=form.nombre.data,
            email=form.email.data
        )
        return redirect(url_for("socios.listar"))

    return render_template("paginas/socios/socio_editar.html", form=form, socio=socio)