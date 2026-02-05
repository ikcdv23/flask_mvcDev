from flask import Blueprint, render_template, request, redirect, url_for
from app.forms.socio_form import SocioForm
from app.services.socios_service import *
from flask import flash 

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
    # 1. Buscamos el socio (Usa el servicio, evita penalizaciones)
    socio = obtener_socio(id)
    
    if not socio:
        return "Socio no encontrado", 404

    # 2. Rellenamos el formulario con los datos actuales (Clave para R13)
    form = SocioForm(obj=socio)

    # 3. Si le dan a Guardar...
    if form.validate_on_submit():
        # Llamamos al servicio para guardar los cambios
        editar_socio(id, form.nombre.data, form.email.data)
        return redirect(url_for("socios.listar"))
    if request.method == "POST":
        print("ERRORES DE FORMULARIO:", form.errors)
        # 4. Mostramos el HTML que te pasé antes
        return render_template("paginas/socios/socio_editar.html", form=form, socio=socio)


# ruta para borrar el socio, con la lógica de verificación de libros pendientes
@socios_bp.route("/borrar/<int:id>")
def borrar(id):
    exito, mensaje = borrar_socio(id)
    flash(mensaje)  # Usamos flash para mostrar el mensaje al usuario
    return redirect(url_for("socios.listar"))