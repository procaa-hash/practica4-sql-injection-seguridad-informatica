"""
escaneo_red.py
==============
LABORATORIO CONTROLADO - USO ACADÉMICO EXCLUSIVO
Asignatura: Seguridad Informática (UNEMI)

PROPÓSITO
---------
Módulo complementario de escaneo básico de puertos/servicios. Por diseño,
el objetivo por defecto es 127.0.0.1 (el propio equipo). El escaneo de
puertos sobre equipos ajenos sin autorización explícita puede ser ilegal;
este módulo solo debe usarse sobre sistemas propios o de laboratorio.

Utiliza únicamente la librería estándar de Python (socket), verificando qué
puertos comunes se encuentran abiertos y qué servicio suele asociarse a ellos.

Uso:
    python escaneo_red.py            # escanea 127.0.0.1
    python escaneo_red.py 127.0.0.1  # objetivo explícito
"""

import socket
import sys

# Puertos comunes y su servicio típico (referencia IANA).
PUERTOS_COMUNES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5000: "Flask/App laboratorio",
    5432: "PostgreSQL",
    8080: "HTTP alternativo",
}


def escanear_puerto(host: str, puerto: int, timeout: float = 0.5) -> bool:
    """Devuelve True si el puerto TCP está abierto en el host indicado."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            return s.connect_ex((host, puerto)) == 0
        except socket.error:
            return False


def escanear_host(host: str) -> list:
    print("=" * 60)
    print(f" ESCANEO BÁSICO DE PUERTOS - objetivo: {host}")
    print("=" * 60)
    abiertos = []
    for puerto, servicio in sorted(PUERTOS_COMUNES.items()):
        if escanear_puerto(host, puerto):
            abiertos.append((puerto, servicio))
            print(f"  [ABIERTO]  {puerto:>5}/tcp  {servicio}")
        else:
            print(f"  [cerrado]  {puerto:>5}/tcp  {servicio}")
    print("-" * 60)
    print(f"Puertos abiertos detectados: {len(abiertos)}")
    return abiertos


if __name__ == "__main__":
    objetivo = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    if objetivo not in ("127.0.0.1", "localhost"):
        print("AVISO: escanee únicamente equipos propios o de laboratorio,")
        print("       con autorización explícita.\n")
    escanear_host(objetivo)
