# ARCHIVO DE PRUEBAS
import socket
import json

cliente = socket.socket()
cliente.connect(("localhost", 8000))

peticion = {"buscar_medico"}

cliente.send(
    json.dumps(peticion).encode("utf-8"))

respuesta = cliente.recv(4096)
print(respuesta.decode("utf-8"))

cliente.close()
