
from ..dataclass import Agenda, User
from ..dbcom import DBCom, dbcom

class AgendaDAO:
    def __init__(self, s: DBCom):
        self.dbcom = s
        
    def insert(self, user: User, agenda: Agenda) -> Agenda:
        self.dbcom.sendall({
            "data":{
                "user_id": user.id,
                "name": agenda.name
            },
            "requestType": "createAgenda",
            "op": 3
        })
        r = self.dbcom.recv()
        agenda.id = r["data"]["agenda_id"]
        return agenda

    def update(self, agenda: Agenda):
        self.dbcom.sendall({
            "data":{
                "name": agenda.name,
                "agenda_id": agenda.id
            },
            "requestType": "updateAgenda",
            "op": 3
        })
        return self.dbcom.recv()

    def delete(self, agenda: Agenda):
        self.dbcom.sendall({
            "data":{
                "agenda_id": agenda.id
            },
            "requestType": "deleteAgenda",
            "op": 3
        })
        return self.dbcom.recv()
    
    def get_list(self, user: User) -> list[Agenda]:
        self.dbcom.sendall({
            "data": {
                "user_id": user.id
            },
            "requestType": "getAgendaList",
            "op": 3
        })
        r: list[Agenda] = []
        data: dict = self.dbcom.recv()
        for agenda in data["data"]["agendaList"]:
            r.append(Agenda(agenda["id"], agenda["name"]))

        return r
    
    def share(self, mail_receiver: str, agenda: Agenda):
        self.dbcom.sendall({
            "data": {
                "agenda_id": agenda.id,
                "mail": mail_receiver
            },
            "requestType": "shareAgenda",
            "op": 3
        })

        return self.dbcom.recv()
    
    def accept_shared_agenda(self, user: User, agenda: Agenda):
        self.dbcom.sendall({
            "data": {
                "user_id": user.id,
                "agenda_id": agenda.id
            },
            "requestType": "acceptSharedAgenda",
            "op": 3
        })

        return self.dbcom.recv()
    
    def deny_shared_agenda(self, user: User, agenda: Agenda):
        self.dbcom.sendall({
            "data": {
                "user_id": user.id,
                "agenda_id": agenda.id
            },
            "requestType": "denySharedAgenda",
            "op": 3
        })

        return self.dbcom.recv()
    
    def get_pending_agenda_list(self, user: User) -> list[Agenda]:
        self.dbcom.sendall({
            "data": {
                "user_id": user.id
            },
            "requestType": "getPendingAgendaList",
            "op": 3
        })

        r: list[Agenda] = []
        data: dict = self.dbcom.recv()
        for agenda in data["data"]["agendaList"]:
            r.append(Agenda(agenda["id"], agenda["name"]))

        return r

agendadao = AgendaDAO(dbcom)
agendalist: list[Agenda] = []
pendingsharedagendalist: list[Agenda] = []
