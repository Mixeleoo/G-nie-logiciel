import socket
import json

class DBCom:
    def __init__(self, HOST: str, PORT: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect((HOST, PORT))

    def sendall(self, data: dict):
        print("Message à envoyer au serveur :", data)
        self.socket.sendall(json.dumps(data).encode())

    def recv(self) -> dict:
        data_str: str = self.socket.recv(1024).decode()
        print("Message raw reçu du serveur :", data_str)
        data: dict = json.loads()
        print("Message reçu du serveur :", data)
        return data
    
HOST = '127.0.0.1'  # Adresse du serveur
PORT = 65439       # Port du serveur

dbcom = DBCom(HOST, PORT)
