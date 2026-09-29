# Laboratorio de SQL Injection — Seguridad Informática (UNEMI)

**Práctica N.º 4 — Seguridad en redes LAN e inalámbricas y de bases de datos**
Asignatura: Seguridad Informática · Carrera: Tecnologías de la Información (En Línea)
Docente: Ing. Alex Armando Ávila Coello · Período académico 2026

> ⚠️ **Aviso ético y legal.** Todo el contenido de este repositorio es un
> laboratorio **controlado y educativo** que se ejecuta exclusivamente en
> `localhost` (127.0.0.1). Su finalidad es **defensiva**: comprender cómo se
> origina una Inyección SQL y cómo se corrige. No debe desplegarse en producción
> ni emplearse contra sistemas de terceros sin autorización explícita.

## Descripción del proyecto

Entorno web deliberadamente vulnerable construido con **Python + Flask** y una
base de datos **SQLite**, que permite demostrar de forma práctica el ataque de
**Inyección SQL (SQLi — OWASP A03:2021)** y su mitigación mediante **consultas
parametrizadas** (sentencias preparadas).

## Componentes

| Archivo | Descripción |
|---|---|
| `app_vulnerable.py` | Servidor web Flask con formulario de login. Interruptor `SEGURO` para alternar entre versión vulnerable y versión mitigada. |
| `ataque_sql_i.py` | Script de pruebas que envía payloads de bypass (`' OR '1'='1`, `admin'--`) contra la app local. |
| `escaneo_red.py` | Módulo complementario de escaneo básico de puertos/servicios sobre `127.0.0.1`. |
| `MANUAL_USO.md` | Guía paso a paso de instalación, ejecución, ataque y validación del parche. |

## Requisitos

- Python 3.10+
- Flask (`pip install flask`)

## Ejecución rápida

```bash
pip install flask
python app_vulnerable.py      # abre http://127.0.0.1:5000/
python ataque_sql_i.py        # en otra terminal
python escaneo_red.py         # escaneo de localhost
```

Consulte `MANUAL_USO.md` para el procedimiento completo con capturas.

## Contramedida

La defensa se activa cambiando `SEGURO = True` en `app_vulnerable.py`. Con ello
la consulta pasa de concatenación insegura de cadenas a consulta parametrizada:

```python
# Vulnerable
"SELECT ... WHERE usuario = '" + usuario + "' AND clave = '" + clave + "'"

# Seguro (parametrizado)
cur.execute("SELECT ... WHERE usuario = ? AND clave = ?", (usuario, clave))
```

## Licencia y uso

Uso académico exclusivo. Elaborado por el Grupo 17 de Seguridad Informática, UNEMI, 2026.
