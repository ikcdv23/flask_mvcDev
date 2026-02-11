Al utilizar el proyecto hay que crear el directorio venv con :
python -m venv venv

Despues hay que instalar las dependencias con :
pip install -r requirements.txt

Siempre que se instalen nuevas dependencias hay que actualizar el archivo requirements.txt con:
pip freeze > requirements.txt



==== COMANDOS ÚTILES ====
- Crear la carpeta de trabajo: primer_flask
- Abrir cmd o powershell en la carpeta
- Crear el entorno virtual: python -m venv venv 
- Esto crea una carpeta venv que contiene todo el entorno Python del proyecto.
- Activar el entorno: venv\Scripts\activate
- Instalar Flask: pip install flask
- Mirar los paquetes instalados: pip freeze

# Flask MVC - Sistema de Gestión de Biblioteca

Este proyecto implementa una arquitectura MVC (Modelo-Vista-Controlador) estricta con una **capa de servicios intermedia**, garantizando un código desacoplado, escalable y mantenible.  

Incluye autenticación segura, gestión de roles y protección frente a vulnerabilidades web comunes.

---

## Características Principales

### Gestión de Libros (CRUD)
- Alta, baja, modificación y consulta de libros.

### Gestión de Socios (CRUD)
- Administración completa de usuarios lectores.

### Sistema de Préstamos
- Lógica de negocio para asignación y devolución de libros.
- Vinculación entre libros y socios.

### Seguridad
- Autenticación de usuarios (Login/Logout) mediante **Flask-Login**.
- Contraseñas encriptadas mediante **hash SHA-256**.
- Protección **CSRF** en todos los formularios (Flask-WTF).
- Decoradores personalizados `@role_required` para proteger rutas administrativas.

### Interfaz
- Diseño responsivo con CSS personalizado.

---

## Arquitectura del Proyecto

El sistema sigue una arquitectura por capas que separa claramente las responsabilidades:

### Controladores (Controllers)
- Gestionan las rutas HTTP.
- Validan formularios.
- No acceden directamente a la base de datos.
- Delegan la lógica de negocio a los servicios.

### Servicios (Services)
- Contienen la lógica de negocio.
- Aplican reglas de préstamos y validaciones complejas.
- Son la única capa que interactúa con los modelos.

### Modelos (Models)
- Representan las tablas de la base de datos mediante **SQLAlchemy**.

### Vistas (Templates)
- Archivos HTML renderizados con **Jinja2**.

---

## Estructura del Proyecto

flask_mvcDev/
├── app/
│ ├── controllers/ # Rutas y lógica de control (auth, libros, socios)
│ ├── models/ # Definición de tablas (Libro, Socio, Usuario)
│ ├── services/ # Lógica de negocio
│ ├── forms/ # Formularios y validaciones (WTForms)
│ ├── templates/ # Vistas HTML (Jinja2)
│ ├── static/ # CSS, JS e imágenes
│ ├── decorators.py # Decorador de seguridad personalizado
│ └── init.py # Configuración inicial de la aplicación y base de datos
├── instance/ # Base de datos SQLite
├── run.py # Punto de entrada de la aplicación
└── requirements.txt # Dependencias del proyecto

## Instalación y Ejecución

### 1. Preparar el entorno

# Acceder a la carpeta del proyecto
cd flask_mvcDev

# (Opcional) Crear y activar un entorno virtual
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate

# Para instalar las dependencias haremos uso de requirements.txt
pip install -r requirements.txt