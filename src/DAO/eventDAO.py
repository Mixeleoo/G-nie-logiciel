
<<<<<<< HEAD
from src.dataclass.event import Event
from src.dataclass.agenda import Agenda
from src.dataclass.color import Color
from src.dbcom import DBCom, dbcom
=======
from ..dataclass import Event, Agenda, Color
from ..dbcom import DBCom, dbcom
>>>>>>> 0ed2231 (on va prier)

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
                "cancel": event.cancel,
                "start": event.start,
                "end": event.end,
                "color": (event.color.r << 16) | (event.color.g << 8) | event.color.b,
                "frequency": event.frequency,
                "interval": event.interval,
                "by_day": event.by_day,
                "by_month_day": event.by_month_day,
                "until": event.until
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
                    event["cancel"],
                    event["start"],
                    event["end"],
                    Color(
                        r=(event["color"] >> 16) & 0xFF,
                        g=(event["color"] >> 8) & 0xFF,
                        b=event["color"] & 0xFF
                    ),
                    event["frequency"],
                    event["interval"],
                    event["by_day"],
                    event["by_month_day"],
                    event["until"]
                )
            )

        return r

eventdao = EventDAO(dbcom)
