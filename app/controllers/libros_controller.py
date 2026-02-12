from flask import Blueprint,  request, render_template, redirect, url_for, flash
from app.forms.libro_form import LibroForm

from app.forms.prestamos_form import PrestamosForm
from app.forms.buscar_form import BuscarForm

from app.services.libros_service import *

# para poder indicar que funciones son exclusivas de admin
from app.decorators import role_required



from flask import request

libros_bp = Blueprint(
    "libros",
    __name__,
    url_prefix="/libros"
)
#ruta para listar
@libros_bp.route("/")
def listar():
    libros = listar_libros()
    # devuelve la vista de listar libros
    return render_template("paginas/libros/libros.html", libros=libros) 

# Ruta para ver el libro elegido
@libros_bp.route("/<int:id>")
def ver(id):
    libro = obtener_libro(id)
    if not libro:
        return "Libro no encontrado", 404
    return render_template("paginas/libros/libro_ver.html", libro=libro)

# Ruta para ver los libros en formato grid
# he modificado la funcion de grid para que permita implementar un buscador
@libros_bp.route("/grid", methods=["GET"])
def grid():
    form = BuscarForm(request.args)
    busqueda_activa = False
    
    # Capturamos si el usuario ha pulsado el botón "Ver Disponibles"
    filtro_activo = request.args.get('filtro') # Puede ser 'disponibles' o None

    if form.validate() and form.busqueda.data:
        # 1. Si busca algo, prioridad al buscador
        libros = buscar_libros(form.busqueda.data)
        busqueda_activa = True
    elif filtro_activo == 'disponibles':
        # 2. Si no busca, pero quiere ver disponibles (R2)
        libros = listar_libros_disponibles()
    else:
        # 3. Si no hay nada, mostrar todo
        libros = listar_libros()

    return render_template(
        "paginas/libros/librosGrid.html", 
        libros=libros, 
        form=form, 
        busqueda=busqueda_activa,
        filtro_activo=filtro_activo 
    )
    
    
#ruta para crear un libro
@libros_bp.route("/crear", methods=["GET", "POST"])
# indica que para esta funcion es necesario ser admin
@role_required("admin")
def crear():
    form = LibroForm()
    if request.method == "POST":
        if form.validate_on_submit():
            titulo = form.titulo.data
            autor = form.autor.data
            anio = form.anio.data
            categoria = form.categoria.data
            # No pasamos id_socio, el libro nace disponible

            crear_libro(titulo, autor, anio, categoria)

            return redirect(url_for("libros.listar"))

    return render_template("paginas/libros/libro_crear.html", form=form)

# Ruta para editar un libro 
@libros_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@role_required("admin")
def editar(id):
    libro = obtener_libro(id)
    
    if not libro:
        return "Libro no encontrado", 404

    form = LibroForm(obj=libro)

    if form.validate_on_submit():

        editar_libro(
            libro_id=id,
            titulo=form.titulo.data,
            autor=form.autor.data,
            anio=form.anio.data,
            categoria=form.categoria.data
            # Nota, No editamos el socio aquí. Eso se hace en "Prestar"
        )
        return redirect(url_for("libros.listar"))

    # 5. Mostramos la plantilla. Pasamos 'libro' para poder poner el título en la cabecera si queremos.
    return render_template("paginas/libros/libro_editar.html", form=form, libro=libro)

@libros_bp.route("/prestar/<int:id>", methods=["GET", "POST"])
@role_required("admin")
def prestar(id):
    libro = obtener_libro(id) # Verificar el libro
    form = PrestamosForm() 
    
    # Llenar el desplegable con los socios (R5)
    from app.services.socios_service import listar_socios
    form.socio_id.choices = [(s.id, s.nombre) for s in listar_socios()]

    if form.validate_on_submit():
        # Aquí llamas al servicio para guardar el préstamo (R5, R6)
        prestar_libro(id, form.socio_id.data)
        return redirect(url_for('libros.ver', id=id))

    return render_template("paginas/libros/libro_prestar.html", form=form, libro=libro)


## Ruta para cancelar reserva
@libros_bp.route("/cancelar_reserva/<int:id>")
@role_required("admin")
def cancelar_reserva(id):
    # Llamamos a la lógica que acabamos de crear
    devolver_libro(id)
    
    # Te manda SIEMPRE al grid (como tú querías)
    return redirect(url_for("libros.grid"))

### ruta para eliminar un libro
@libros_bp.route("/eliminar/<int:id>")
@role_required('admin') # Solo el admin puede borrar
def eliminar(id):
    # Llamamos al servicio
    exito, mensaje = eliminar_libro(id)
    
    if exito:
        flash(mensaje, "success")
    else:
        # Si falló (por estar prestado o error), mostramos error rojo
        flash(mensaje, "danger")
        
    return redirect(url_for('libros.grid'))