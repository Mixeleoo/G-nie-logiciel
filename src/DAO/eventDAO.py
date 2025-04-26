
from dataclass import Event, Agenda
from dbcom import DBCom

class EventDAO:
    def __init__(self, s: DBCom):
        self.dbcom = s

    def insert(self, agenda: Agenda, event: Event):
        self.dbcom.sendall({
            "data":{
                "agenda_id": agenda.id,
                "name": event.name
            },
            "requestType": "createEvent",
            "op": 3
        })
        return self.dbcom.recv()

    def update(self, event: Event):
        self.dbcom.sendall({
            "data":{
                "name": event.name,
                "cancel": int(event.cancel),
                "event_id": event.id
            },
            "requestType": "updateEvent",
            "op": 3
        })
        return self.dbcom.recv()

    def delete(self, event: Event):
        self.s.sendall({
            "data":{
                "event_id": event.id
            },
            "requestType": "deleteEvent",
            "op": 3
        })
        return self.dbcom.recv()

    def cancel(self, event: Event):
        event.cancel = True
        return self.update(event)

    def get_list(self, agenda: Agenda) -> list[Event]:
        self.dbcom.sendall({
            "data": {
                "agenda_id": agenda.id
            },
            "requestType": "getEventList",
            "op": 3
        })
        r: list[Event] = []
        data: dict = self.dbcom.recv()
        for event in data["data"]["eventList"]:
            r.append(Event(event["id"], event["name"], event["cancel"]))

        return r
