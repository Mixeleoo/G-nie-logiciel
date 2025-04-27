
from dataclass import Event, Agenda, Color
from dbcom import DBCom, dbcom

class EventDAO:
    def __init__(self, s: DBCom):
        self.dbcom = s

    def insert(self, agenda: Agenda, event: Event):
        """
        création d'un event
        """
        self.dbcom.sendall({
            "data":{
                "agenda_id": agenda.id,
                "name": event.name,
                "desc": event.desc,
                "cancel": event.cancel,
                "start": event.start,
                "end": event.end,
                "color": (event.color.r << 16) | (event.color.g << 8) | event.color.b
            },
            "requestType": "createEvent",
            "op": 3
        })
        return self.dbcom.recv()

    def update(self, event: Event):
        """
        update l'event
        """
        self.dbcom.sendall({
            "data":{
                "name": event.name,
                "desc": event.desc,
                "cancel": int(event.cancel),
                "start": event.start,
                "end": event.end,
                "color": (event.color.r << 16) | (event.color.g << 8) | event.color.b,
                "event_id": event.id
            },
            "requestType": "updateEvent",
            "op": 3
        })
        return self.dbcom.recv()

    def delete(self, event: Event):
        """
        supprimer un event != annuler un event
        """
        self.dbcom.sendall({
            "data":{
                "event_id": event.id
            },
            "requestType": "deleteEvent",
            "op": 3
        })
        return self.dbcom.recv()

    def cancel(self, event: Event):
        """
        annuler un event != supprimer un event
        """
        event.cancel = True
        return self.update(event)

    def get_list(self, agenda: Agenda) -> list[Event]:
        """
        récupérer la liste des évènements d'un agenda, fonctionne pour les agendas appartenant à l'utilisateur mais également les agendas partagés
        """
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
            r.append(
                Event(
                    event["id"],
                    event["name"],
                    event["desc"],
                    event["cancel"],
                    event["start"],
                    event["end"],
                    Color(
                        r=(event["color"] >> 16) & 0xFF,
                        g=(event["color"] >> 8) & 0xFF,
                        b=event["color"] & 0xFF
                    )
                )
            )

        return r

eventdao = EventDAO(dbcom)
