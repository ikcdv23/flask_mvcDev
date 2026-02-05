from flask import Blueprint,  request, render_template, redirect, url_for
from app.forms.libro_form import LibroForm
from app.services.libros_service import *
from app.forms.prestamos_form import PrestamosForm

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
@libros_bp.route("/grid")
def grid():
    libros = listar_libros()
    return render_template("paginas/libros/librosGrid.html", libros=libros)

#ruta para crear un libro
@libros_bp.route("/crear", methods=["GET", "POST"])
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
            # Nota: No editamos el socio aquí. Eso se hace en "Prestar"
        )
        return redirect(url_for("libros.listar"))

    # 5. Mostramos la plantilla. Pasamos 'libro' para poder poner el título en la cabecera si queremos.
    return render_template("paginas/libros/libro_editar.html", form=form, libro=libro)

@libros_bp.route("/prestar/<int:id>", methods=["GET", "POST"])
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

# Ruta para devolver el libro (R11)
@libros_bp.route("/cancelar_reserva/<int:id>")
def cancelar_reserva(id):
    # Llamamos al servicio para limpiar el socio del libro
    from app.services.libros_service import devolver_libro
    devolver_libro(id)
    
    # Redirigimos al grid para ver el cambio
    return redirect(url_for("libros.grid"))