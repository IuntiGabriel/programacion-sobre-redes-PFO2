#!/usr/bin/env python3
# cliente.py
import requests
from requests.auth import HTTPBasicAuth
import sys

BASE = "http://127.0.0.1:5000"

def registro(usuario, contraseña):
    url = f"{BASE}/registro"
    r = requests.post(url, json={"usuario": usuario, "contraseña": contraseña})
    print("STATUS:", r.status_code)
    print(r.json())

def login(usuario, contraseña):
    url = f"{BASE}/login"
    r = requests.post(url, json={"usuario": usuario, "contraseña": contraseña})
    print("STATUS:", r.status_code)
    try:
        print(r.json())
    except:
        print(r.text)

def ver_tareas(usuario, contraseña):
    url = f"{BASE}/tareas"
    r = requests.get(url, auth=HTTPBasicAuth(usuario, contraseña))
    print("STATUS:", r.status_code)
    if r.status_code == 200:
        print("HTML recibido:")
        print(r.text)
    else:
        print("Respuesta:", r.text)

def usage():
    print("Uso:")
    print("  cliente.py registro <usuario> <contraseña>")
    print("  cliente.py login <usuario> <contraseña>")
    print("  cliente.py tareas <usuario> <contraseña>")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage(); sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "registro" and len(sys.argv) == 4:
        registro(sys.argv[2], sys.argv[3])
    elif cmd == "login" and len(sys.argv) == 4:
        login(sys.argv[2], sys.argv[3])
    elif cmd == "tareas" and len(sys.argv) == 4:
        ver_tareas(sys.argv[2], sys.argv[3])
    else:
        usage()
