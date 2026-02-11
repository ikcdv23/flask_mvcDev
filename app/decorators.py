from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 1. ¿Está logueado? Si no, al Login.
            if not current_user.is_authenticated:
                flash("Debes iniciar sesión para acceder a esta función.", "warning")
                return redirect(url_for('auth.login'))

            # 2. ¿Es Admin? (Validamos que el usuario se llame 'admin')
            # Según R116 un único usuario admin es suficiente.
            if role_name == 'admin' and current_user.username != 'admin':
                # Si está logueado pero no es admin, error 403 (Prohibido)
                abort(403)

            # Si pasa las dos pruebas, ejecuta la función original
            return f(*args, **kwargs)
        return decorated_function
    return decorator