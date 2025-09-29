#!/usr/bin/env python3
# servidor.py
from flask import Flask, request, jsonify, render_template_string, g, Response
import sqlite3
import os
import bcrypt
from functools import wraps

DB_PATH = "tareas.db"
app = Flask(__name__)

# -------------------------
# conexion a la BD
# -------------------------
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# -------------------------
# inicializar la DB
# -------------------------
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                password BLOB NOT NULL
            );
        """)
        # tabla de tareas opcional PARA FUTURAS IMPLEMENTACIONES
        cursor.execute("""
            CREATE TABLE tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            );
        """)
        conn.commit()
        conn.close()
        print("Base de datos inicializada en", DB_PATH)
    else:
        print("Base de datos existente:", DB_PATH)

# -------------------------
# verifica credenciales (bcrypt)
# -------------------------
def verify_credentials(usuario, password_plain):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM usuarios WHERE usuario = ?", (usuario,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return False, None
    user_id, hashed = row[0], row[1]
    # hashed es bytes (BLOB)
    if isinstance(hashed, str):
        # Por si se guardó como TEXT: convertir a bytes SEGURIDAD A VECES PASA
        hashed = hashed.encode("utf-8")
    ok = bcrypt.checkpw(password_plain.encode("utf-8"), hashed)
    return ok, user_id if ok else (False, None)

# -------------------------
# pop up Basic Auth
# -------------------------
def requires_basic_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return Response(
                'Authentication required', 401,
                {'WWW-Authenticate': 'Basic realm="Login required"'}
            )
        usuario = auth.username
        password = auth.password or ""
        ok, user_id = verify_credentials(usuario, password)
        if not ok:
            return Response('Invalid credentials', 401,
                            {'WWW-Authenticate': 'Basic realm="Login required"'})
        # inyectar user info en kwargs EVITA REPETICION
        return f(usuario=usuario, user_id=user_id, *args, **kwargs)
    return decorated

# -------------------------
# Endpoint: POST /registro
# Recibe JSON: {"usuario": "...", "contraseña": "..."}
# -------------------------
@app.route("/registro", methods=["POST"])
def registro():
    if not request.is_json:
        return jsonify({"error": "Se requiere JSON"}), 400
    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("contraseña")

    if not usuario or not password:
        return jsonify({"error": "Faltan datos: 'usuario' y 'contraseña' requeridos"}), 400

    # generar hash con bcrypt
    salt = bcrypt.gensalt()  # por defecto rounds razonables
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)  # bytes

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (?, ?)", (usuario, hashed))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Usuario registrado con éxito"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409
    except Exception as e:
        return jsonify({"error": "Error al registrar", "detalle": str(e)}), 500

# -------------------------
# Endpoint: POST /login
# Recibe JSON: {"usuario": "...", "contraseña": "..."}
# Verifica credenciales y devuelve mensaje
# -------------------------
@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"error": "Se requiere JSON"}), 400
    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("contraseña")

    if not usuario or not password:
        return jsonify({"error": "Faltan datos: 'usuario' y 'contraseña'"}), 400

    ok, user_id = verify_credentials(usuario, password)
    if ok:
        return jsonify({"mensaje": f"Inicio de sesión exitoso. Bienvenido {usuario}", "usuario_id": user_id}), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

# -------------------------
# Endpoint: GET /tareas
# Requiere HTTP Basic Auth; muestra HTML de bienvenida
# -------------------------
@app.route("/tareas", methods=["GET"])
@requires_basic_auth
def tareas(usuario=None, user_id=None):
    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>Gestion de tareas - Bienvenido</title>
      </head>
      <body>
        <h1>Bienvenido a la API de tareas</h1>
        <p>Usuario autenticado: <strong>{usuario}</strong> (id: {user_id})</p>
        <p>PAGINA DE BIENVENIDA</p>
        Aca en el futuro podras ver una hermosa pagina que se encuentra en construccion.
      </body>
    </html>
    """
    return render_template_string(html), 200

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    init_db()
    # ejecutar en 0.0.0.0 para acceso desde lan
    app.run(host="0.0.0.0", port=5000, debug=True)
