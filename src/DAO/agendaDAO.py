
from dataclass import Agenda, User
from dbcom import DBCom

class AgendaDAO:
    def __init__(self, s: DBCom):
        self.dbcom = s
        
    def insert(self, user: User, agenda: Agenda):
        self.dbcom.sendall({
            "data":{
                "user_id": user.id,
                "name": agenda.name
            },
            "requestType": "createAgenda",
            "op": 3
        })
        return self.dbcom.recv()

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
        self.s.sendall({
            "data":{
                "agenda_id": agenda.id
            },
            "requestType": "deleteAgenda",
            "op": 3
        })
        return self.dbcom.recv()
    
    def get_agenda_list(self, user: User) -> list[Agenda]:
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
