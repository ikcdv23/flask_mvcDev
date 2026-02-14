# Flask MVC - Sistema de Gestión de Biblioteca

Proyecto web desarrollado con Flask que implementa una arquitectura MVC con una capa de servicios intermedia. Permite gestionar libros, socios y préstamos, e incluye sistema de autenticación, roles y protección CSRF.

## Guía de Instalación

Sigue estos pasos en orden estricto para configurar y ejecutar el proyecto en tu equipo local:

1. **Accede a la carpeta del proyecto**
   Abre tu terminal (CMD o PowerShell) y navega hasta el directorio:

   cd flask_mvcDev



2. **Crea el entorno virtual**
Esto generará una carpeta `venv` aislada para las dependencias del proyecto:

python -m venv venv



3. **Activa el entorno virtual**
* En Windows (CMD/PowerShell):

venv\Scripts\activate




* En Mac/Linux:

source venv/bin/activate






4. **Instala las dependencias**
Lee el archivo de requerimientos e instala los paquetes necesarios:

pip install -r requirements.txt



5. **Ejecuta la aplicación**
Inicia el servidor local de Flask:

python run.py

## Estructura del Proyecto

```text
flask_mvcDev/
├── app/
│   ├── controllers/   # Rutas HTTP y validación de peticiones
│   ├── models/        # Modelos de base de datos (SQLAlchemy)
│   ├── services/      # Lógica de negocio y reglas de la aplicación
│   ├── forms/         # Definición de formularios (WTForms)
│   ├── templates/     # Vistas HTML (Jinja2)
│   ├── static/        # Archivos estáticos (CSS, JS)
│   ├── decorators.py  # Decoradores personalizados (ej. protección de rutas)
│   └── __init__.py    # Configuración inicial de Flask y extensiones
├── instance/          # Base de datos SQLite local
├── run.py             # Punto de entrada para levantar el servidor
└── requirements.txt   # Lista de dependencias de Python


## Mantenimiento de Dependencias

Si durante el desarrollo instalas un paquete nuevo (por ejemplo, `pip install nuevo_paquete`), debes actualizar el registro para que otros desarrolladores puedan instalarlo:


pip freeze > requirements.txt

