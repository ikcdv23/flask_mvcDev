from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.forms.auth_form import LoginForm

# IMPORTANTE: Importamos el servicio, NO el modelo ni la DB
from app.services.auth_service import verificar_credenciales, crear_usuario_admin

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        # EL CAMBIO CLAVE:
        # El controlador delega la lógica al servicio.
        # Le dice: "Toma estos datos y dime si el usuario es válido".
        usuario_valido = verificar_credenciales(form.username.data, form.password.data)
        
        if usuario_valido:
            # login_user gestiona la cookie de sesión (esto sí es tarea del controlador/flask)
            login_user(usuario_valido) 
            return redirect(url_for('libros.grid'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user() # Gestión de sesión (HTTP), correcto en controlador
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('auth.login'))

# RUTA PARA CREAR ADMIN (Refactorizada)
@auth_bp.route('/crear-admin')
def crear_admin():
    # Delegamos la creación al servicio
    exito = crear_usuario_admin('admin', '1234')
    
    if exito:
        return "Admin creado correctamente"
    else:
        return "El usuario admin ya existía o hubo un error"