# Sistema de Gestión de Tareas con API y Base de Datos

Este proyecto implementa una **API REST** con **Flask**, utilizando **SQLite** para la persistencia de datos y **bcrypt** para proteger las contraseñas.  
Permite registrar usuarios, iniciar sesión y acceder a una página de bienvenida para la gestión de tareas.

---

## Objetivos del proyecto
Al finalizar este trabajo práctico se busca que el estudiante sea capaz de:

1. Implementar una **API REST** con endpoints funcionales.
2. Utilizar **autenticación básica** con protección de contraseñas.
3. Gestionar datos persistentes con **SQLite**.
4. Construir un **cliente en consola** que interactúe con la API.

---

## Tecnologias utilizadas
- [Python 3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [SQLite](https://www.sqlite.org/)
- [bcrypt](https://pypi.org/project/bcrypt/)
- [cURL](https://curl.se/) (para pruebas rápidas de la API)

---

## Instalación y configuración

### Clonar el repositorio
```bash
git clone https://github.com/IuntiGabriel/programacion-sobre-redes-PFO2.git
cd cd programacion-sobre-redes-PFO2/
```

### Crear un entorno virtual - altamente recomendable trabajar en un entorno virtual para evitar conflictos de dependencias.
```bash
python -m venv venv
```

#### Activa el entorno virtual
# Windows Powershell
```bash
venv\Scripts\Activate
```

# Linux - MAC
```bash
source venv/bin/activate
```

#### Instalar dependendias
```bash
pip install -r requirements.txt
```

# Si el archivo requirements.txt no existe podes instalar las dependencias manualmente
```bash
pip install flask bcrypt requests
```

## Ejecutar el servidor 
```bash
python servidor.py
```

### Por defecto Flask corre en:
http://127.0.0.1:5000


## Endpoint disponibles
### REGISTRO DE USUARIOS POST /registro
### INICIO DE SESION POST /login
### PAGINA DE BIENVENIDA GET /tareas
http://127.0.0.1:5000/tareas 

Método	Endpoint	Descripción	                        Requiere Autenticación
POST	/registro	Registra un nuevo usuario.	        No
POST	/login	    Inicia sesión y obtiene un token.	No
GET	    /tareas	    Muestra las tareas del usuario.	    Sí