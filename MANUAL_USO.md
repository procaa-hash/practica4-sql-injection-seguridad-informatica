# Manual de Uso y Pruebas

**Proyecto:** Laboratorio de SQL Injection — Flask + SQLite
**Asignatura:** Seguridad Informática (UNEMI) · Práctica N.º 4 · 2026

> Laboratorio controlado. Todos los comandos se ejecutan en el equipo propio
> del estudiante (`localhost`). Uso académico y defensivo.

---

## 1. Requisitos previos

- Python 3.10 o superior (`python --version`)
- Editor Visual Studio Code
- Git / GitHub (para el control de versiones)

## 2. Instalación

```bash
# 1. Clonar o descargar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd proyecto_sqli

# 2. Instalar la dependencia
pip install flask
```

*(Captura sugerida 1: terminal mostrando `pip install flask` finalizado.)*

## 3. Ejecución del servidor local

Verifique que en `app_vulnerable.py` la variable esté en modo vulnerable:

```python
SEGURO = False
```

Inicie el servidor:

```bash
python app_vulnerable.py
```

Salida esperada:

```
Base de datos de laboratorio inicializada.
Modo: VULNERABLE  ->  http://127.0.0.1:5000/
```

Abra en el navegador: **http://127.0.0.1:5000/**

*(Captura sugerida 2: formulario de login en modo VULNERABLE.)*

## 4. Prueba de ataque ANTES de la mitigación

### 4.1 Prueba manual (navegador)

En el campo **Usuario** escriba el siguiente payload y cualquier clave:

```
admin' OR '1'='1
```

Resultado: **Acceso concedido** sin conocer la contraseña → *bypass* de
autenticación exitoso.

*(Captura sugerida 3: mensaje "Acceso concedido" tras el payload.)*

### 4.2 Prueba automatizada (script)

En una segunda terminal:

```bash
python ataque_sql_i.py
```

Salida esperada (resumen):

```
[Credencial legítima (control)]        -> ACCESO CONCEDIDO
[Credencial inválida (control)]        -> acceso denegado
[Bypass de autenticación (SQLi)]       -> ACCESO CONCEDIDO   <-- vulnerabilidad
[Comentario para anular clave (SQLi)]  -> ACCESO CONCEDIDO   <-- vulnerabilidad
```

*(Captura sugerida 4: salida del script de ataque en modo vulnerable.)*

## 5. Aplicación de la contramedida (mitigación)

Detenga el servidor (`Ctrl + C`), edite `app_vulnerable.py` y cambie:

```python
SEGURO = True
```

Vuelva a ejecutar `python app_vulnerable.py`. Ahora la consulta es
**parametrizada**.

## 6. Validación del parche de seguridad

Repita el ataque:

```bash
python ataque_sql_i.py
```

Salida esperada (resumen):

```
[Credencial legítima (control)]        -> ACCESO CONCEDIDO
[Credencial inválida (control)]        -> acceso denegado
[Bypass de autenticación (SQLi)]       -> acceso denegado    <-- neutralizado
[Comentario para anular clave (SQLi)]  -> acceso denegado    <-- neutralizado
```

El login legítimo sigue funcionando y los payloads de inyección quedan
neutralizados. **La vulnerabilidad ha sido corregida.**

*(Captura sugerida 5: salida del script con los ataques denegados.)*

## 7. Módulo de escaneo de red (complementario)

```bash
python escaneo_red.py
```

Escanea puertos comunes en `127.0.0.1` e identifica servicios abiertos
(por ejemplo, el puerto 5000 de la app de laboratorio).

*(Captura sugerida 6: salida del escaneo mostrando el puerto 5000 abierto.)*

## 8. Tabla resumen de resultados

| Prueba | Modo VULNERABLE | Modo SEGURO |
|---|---|---|
| Login legítimo (`pedro`) | Acceso concedido | Acceso concedido |
| Login inválido | Acceso denegado | Acceso denegado |
| `admin' OR '1'='1` | **Acceso concedido** | Acceso denegado |
| `admin'--` | **Acceso concedido** | Acceso denegado |

---

Elaborado por el Grupo 17 de Seguridad Informática — UNEMI, 2026.
