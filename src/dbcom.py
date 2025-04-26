import socket
import json

class DBCom:
    def __init__(self, host: str, port: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect((host, port))

    def sendall(self, data: dict):
        print("Message à envoyer au serveur :", data)
        self.socket.sendall(json.dumps(data).encode())

    def recv(self) -> dict:
        data = json.loads(self.socket.recv(1024).decode())
        print("Message reçu du serveur :", data)
        return data

HOST = '127.0.0.1'  # Adresse du serveur
PORT = 65439       # Port du serveur

dbcom = DBCom(HOST, PORT)
