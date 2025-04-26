import socket
import sqlite3
import json
from typing import Callable
from requests_format import *

con = sqlite3.connect("db.db")

HOST = '127.0.0.1'
PORT = 65439

class Request:
    def __init__(self, query: str, func: Callable[[sqlite3.Cursor], str]):
        self.query = query
        self.func = func

    def send(self, *args) -> str:
        return self.func(con.execute(self.query, args))

requestType_to_query: dict[str, Request] = {
    "updateUser": Request("update user set mail = ?, mdp = ? where id = ?;", updateUser),

    "createAgenda": Request("insert into agenda (user_id, name) values (?, ?);", createAgenda),
    "updateAgenda": Request("update agenda set name = ? where id = ?;", updateAgenda),
    "getAgendaList": Request("select * from agenda where user_id = ?;", getAgendaList),

    "createEvent": Request("insert into event (agenda_id, name) values (?, ?);", createEvent),
    "updateEvent": Request("update event set name = ?, cancel = ? where id = ?;", updateEvent),
    "deleteEvent": Request("delete from event where id = ?;", deleteEvent),
    "getEventList": Request("select * from event where agenda_id = ?;", getEventList)
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Serveur en écoute sur {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print(f"Connecté par {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break

            m_json = json.loads(data)
            print("Reçu du client :", m_json)
            
            # REGISTER
            if m_json["op"] == 1:
                auth = m_json["authentification"]
                cur = con.execute("insert into user (mail, mdp) values (?, ?);", (auth["mail"], auth["mdp"]))
                conn.sendall(str(cur.fetchall()).encode())

            # CONNECT
            elif m_json["op"] == 2:
                auth = m_json["authentification"]
                cur = con.execute("select id from user where mail = ? and mdp = ?;", (auth["mail"], auth["mdp"]))
                users_info = cur.fetchall()
                if not users_info:
                    conn.sendall("{\"errmsg\":\"PAS DE COMPTE\",\"op\":5}".encode())

                else:
                    user_info = users_info[0]
                    conn.sendall(json.dumps({
                        "data":{
                            "id": user_info[0]
                        },
                        "op": 4
                    }).encode())

            elif m_json["op"] == 3:
                try:
                    data: str = requestType_to_query[m_json["requestType"]].send(*m_json["data"].values())
                except sqlite3.Error as e:
                    conn.sendall(("{\"errmsg\":\"" + str(e) + "\",\"op\":5}").encode())
                else:
                    conn.sendall(data.encode())

            con.commit()
