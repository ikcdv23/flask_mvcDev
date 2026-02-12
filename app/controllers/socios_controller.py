from flask import Blueprint, render_template, request, redirect, url_for
from app.forms.socio_form import SocioForm
from app.services.socios_service import *
from flask import flash 
from app.forms.buscar_form import BuscarForm
from app.decorators import role_required

socios_bp = Blueprint(
    "socios",       
    __name__,
    url_prefix="/socios"
)

@socios_bp.route("/")
@role_required('admin') # R17: Ver socios es solo Admin
def listar():
    # 1. Instanciamos el formulario con los datos de la URL (GET)
    form = BuscarForm(request.args)
    
    socios = []
    busqueda_activa = False

    # 2. Si hay algo escrito en el buscador...
    if form.validate() and form.busqueda.data:
        socios = buscar_socios(form.busqueda.data)
        busqueda_activa = True
    else:
        # 3. Si no, listamos todos
        socios = listar_socios()

    # 4. Renderizamos la plantilla pasando el form y los resultados
    return render_template(
        "paginas/socios/socios.html", 
        socios=socios, 
        form=form, 
        busqueda=busqueda_activa
    )

@socios_bp.route("/con-prestamos")
@role_required("admin")
def listar_con_prestamos():
    # Usamos la función especial que creaste en el servicio
    socios = listar_socios_con_libros()
    return render_template("paginas/socios/socios_prestamos.html", socios=socios)

## Ruta para crear un socio 
@socios_bp.route("/crear", methods=["GET", "POST"])
@role_required("admin")
def crear():   
    form = SocioForm()  
    if request.method == "POST":
        if form.validate_on_submit():
            nombre = form.nombre.data
            email = form.email.data           

            crear_socio(nombre, email)         

            return redirect(url_for("socios.listar"))  
    return render_template("paginas/socios/socio_crear.html", form=form)     

## Ruta para editar el socio
@socios_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@role_required("admin")
def editar(id):
    # 1. Buscamos el socio
    socio = obtener_socio(id)
    
    if not socio:
        return "Socio no encontrado", 404
    form = SocioForm(obj=socio)

    # 3. Si le dan a Guardar (POST válido)...
    if form.validate_on_submit():
        editar_socio(id, form.nombre.data, form.email.data)
        return redirect(url_for("socios.listar"))
    if form.errors:
        print("ERRORES DE FORMULARIO:", form.errors)
    return render_template("paginas/socios/socio_editar.html", form=form, socio=socio)

## ver el perfil del socio
@socios_bp.route("/ver/<int:id>")
@role_required("admin")
def ver(id):
    socio = obtener_socio(id)
    if not socio:
        return "Socio no encontrado", 404
    return render_template("paginas/socios/socio_ver.html", socio=socio)

# ruta para borrar el socio, con la lógica de verificación de libros pendientes
@socios_bp.route("/borrar/<int:id>")
@role_required("admin")
def borrar(id):
    exito, mensaje = borrar_socio(id)
    flash(mensaje)  # Usamos flash para mostrar el mensaje al usuario
    return redirect(url_for("socios.listar"))

