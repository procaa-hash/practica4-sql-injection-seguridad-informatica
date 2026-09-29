"""
app_vulnerable.py
=================
LABORATORIO CONTROLADO - USO ACADÉMICO EXCLUSIVO
Asignatura: Seguridad Informática (UNEMI)
Práctica N.º 4 - Escaneo de red, WLAN, BD y SQL Injection

ADVERTENCIA ÉTICA
-----------------
Esta aplicación es DELIBERADAMENTE VULNERABLE y se ejecuta únicamente en
localhost (127.0.0.1) dentro de un entorno de laboratorio aislado. Su único
propósito es DEMOSTRAR, con fines educativos y defensivos, cómo se produce
una Inyección SQL (SQLi) y cómo se corrige. NO debe desplegarse en Internet
ni utilizarse contra sistemas de terceros. El código incluye, junto a la
versión vulnerable, la versión mitigada con consultas parametrizadas.

Ejecución:
    pip install flask
    python app_vulnerable.py
Luego abrir http://127.0.0.1:5000/
"""

import sqlite3
import os
from flask import Flask, request, render_template_string, g

app = Flask(__name__)
DB_PATH = "laboratorio.db"

# Cambie SEGURO = False para observar la vulnerabilidad,
# y SEGURO = True para observar la contramedida (consultas parametrizadas).
SEGURO = False


# --------------------------------------------------------------------------
# Inicialización de la base de datos de laboratorio (SQLite)
# --------------------------------------------------------------------------
def init_db():
    """Crea una base de datos SQLite con datos ficticios para el laboratorio."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE usuarios (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario  TEXT NOT NULL,
            clave    TEXT NOT NULL,
            rol      TEXT NOT NULL
        )
        """
    )
    # Datos de prueba (ficticios, sin valor real)
    datos = [
        ("admin", "S3gur1dad2026", "administrador"),
        ("pedro", "estudiante123", "usuario"),
        ("soporte", "helpdesk2026", "usuario"),
    ]
    cur.executemany(
        "INSERT INTO usuarios (usuario, clave, rol) VALUES (?, ?, ?)", datos
    )
    conn.commit()
    conn.close()


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# --------------------------------------------------------------------------
# Plantilla HTML mínima del formulario de inicio de sesión
# --------------------------------------------------------------------------
PLANTILLA = """
<!doctype html>
<html lang="es">
<head><meta charset="utf-8"><title>Login - Laboratorio SQLi</title></head>
<body style="font-family:Arial;max-width:520px;margin:40px auto;">
  <h2>Inicio de sesión (Laboratorio controlado)</h2>
  <p style="color:#555">Modo actual:
     <b>{{ 'SEGURO (parametrizado)' if seguro else 'VULNERABLE' }}</b></p>
  <form method="POST" action="/login">
    <p>Usuario: <input name="usuario" style="width:100%"></p>
    <p>Clave:   <input name="clave" type="password" style="width:100%"></p>
    <button type="submit">Ingresar</button>
  </form>
  {% if mensaje %}<hr><p><b>Resultado:</b> {{ mensaje }}</p>{% endif %}
  {% if consulta %}<p><b>Consulta ejecutada:</b><br><code>{{ consulta }}</code></p>{% endif %}
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(PLANTILLA, seguro=SEGURO, mensaje=None, consulta=None)


@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario", "")
    clave = request.form.get("clave", "")
    db = get_db()
    cur = db.cursor()

    if not SEGURO:
        # ------------------------------------------------------------------
        # VERSIÓN VULNERABLE: concatenación insegura de cadenas.
        # Un payload como  ' OR '1'='1  rompe la lógica de la consulta.
        # ------------------------------------------------------------------
        consulta = (
            "SELECT usuario, rol FROM usuarios "
            "WHERE usuario = '" + usuario + "' AND clave = '" + clave + "'"
        )
        try:
            filas = cur.execute(consulta).fetchall()
        except Exception as e:
            return render_template_string(
                PLANTILLA, seguro=SEGURO, mensaje=f"Error SQL: {e}", consulta=consulta
            )
    else:
        # ------------------------------------------------------------------
        # VERSIÓN SEGURA (CONTRAMEDIDA): consulta parametrizada.
        # Los datos del usuario nunca se mezclan con el código SQL.
        # ------------------------------------------------------------------
        consulta = "SELECT usuario, rol FROM usuarios WHERE usuario = ? AND clave = ?"
        filas = cur.execute(consulta, (usuario, clave)).fetchall()

    if filas:
        u, rol = filas[0]
        mensaje = f"Acceso concedido. Bienvenido '{u}' (rol: {rol}). Filas: {len(filas)}"
    else:
        mensaje = "Acceso denegado. Credenciales inválidas."

    return render_template_string(
        PLANTILLA, seguro=SEGURO, mensaje=mensaje, consulta=consulta
    )


if __name__ == "__main__":
    init_db()
    print("Base de datos de laboratorio inicializada.")
    print(f"Modo: {'SEGURO' if SEGURO else 'VULNERABLE'}  ->  http://127.0.0.1:5000/")
    # Solo escucha en localhost. Nunca exponer en 0.0.0.0 en un entorno real.
    app.run(host="127.0.0.1", port=5000, debug=False)
