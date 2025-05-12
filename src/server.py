import socket
from typing import Callable
from requests_format import *

con = sqlite3.connect("db.db")

HOST = '127.0.0.1'
PORT = 65439

class Request:
    def __init__(self, query: str, func: Callable[[sqlite3.Cursor], str] = requestSuccess):
        self.query = query
        self.func = func

    def send(self, *args) -> bytes:
        return self.func(con.execute(self.query, args)).encode()

requestType_to_query: dict[str, Request] = {
    "updateUser": Request("update user set mail = ?, mdp = ? where id = ?;"),
    "isUserValid": Request("select 1 from user where mail = ?", isUserValid),

    "createAgenda": Request("insert into agenda (user_id, name) values (?, ?);", createAgenda),
    "updateAgenda": Request("update agenda set name = ? where id = ?;"),
    "getAgendaList": Request("select id, name from agenda where user_id = ?;", getAgendaList),
    "deleteAgenda": Request("delete from agenda where id = ?;"),

    # TODO Récupérer tous les agendas partagés dont la colonne "state" est à 0, pour les mettre dans les demandes d'agenda partagés de l'utilisateur concerné
    "shareAgenda": Request(
            "insert into shared_agenda (user_id, agenda_id)"
            " select id, ? from user where mail = ?;"
        ),
    "acceptSharedAgenda": Request("update shared_agenda set state = 1 where user_id = ? and agenda_id = ?;"),
    "denySharedAgenda": Request("delete from shared_agenda where user_id = ? and agenda_id = ?;"),
    # TODO En même temps que l'on récupère les agenda de l'utilisateur il faudra récupérer les id des agendas dont il a été partagé
    "getPendingAgendaList": Request(
        "select a.id, a.name from shared_agenda sa, agenda a where sa.user_id = ? and state = 0 and sa.agenda_id = a.id;",
        getPendingAgendaList
    ),
    "getSharedAgendaList": Request(
        "select a.id, a.name from shared_agenda sa, agenda a where sa.user_id = ? and state = 1 and sa.agenda_id = a.id;",
        getSharedAgendaList
    ),
    "deleteSharedAgenda": Request("delete from shared_agenda where user_id = ? and agenda_id = ?;"),

    "createEvent": Request(
            "insert into event"
            " (agenda_id, name, cancel, start, 'end', color, frequency, interval, by_day, by_month_day, until)"
            " values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            createEvent
        ),
    "updateEvent": Request(
            "update event"
            " set name = ?, cancel = ?, start = ?, 'end' = ?, color = ?"
            " where id = ?;",
        ),
    "deleteEvent": Request("delete from event where id = ?;"),
    "getEventList": Request("select id, name, cancel, start, 'end', color, frequency, interval, by_day, by_month_day, until from event where agenda_id = ?;", getEventList),

    "createTask": Request("insert into task (user_id, name, desc, done, deadline, color) values (?, ?, ?, ?, ?, ?);"),
    "updateTask": Request("update task set name = ?, desc = ?, done = ?, deadline = ?, color = ? where id = ?;"),
    "deleteTask": Request("delete from task where id = ?;"),
    "getTaskList": Request("select id, name, desc, done, color, deadline from task where user_id = ?;", getTaskList)
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    con.execute("create table if not exists task (id integer primary key, user_id integer references user(id), name text not null default '', desc text not null default '', done bit not null default 0, color integer, deadline integer);")
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
            
            """
            switch op
            case 1: pour la création de compte
            case 2: pour la connexion à un compte
            case 3: requête du client avec comme spécification la catégorie "requestType"
            case 4: retour serveur positif
            case 5: retour serveur négatif avec message d'erreur dans la catégorie "errmsg"
            """

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
                    conn.sendall("{\"errmsg\":\"Pas de compte associant ce mail et mdp\",\"op\":5}".encode())

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
                    data: bytes = requestType_to_query[m_json["requestType"]].send(*m_json["data"].values())
                except sqlite3.Error as e:
                    conn.sendall(("{\"errmsg\":\"" + str(e) + "\",\"op\":5}").encode())
                else:
                    conn.sendall(data)

            con.commit()
