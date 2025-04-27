
import sqlite3
import json

requestSuccess = lambda cur=None: "{\"op\":4}"

def createAgenda(cur: sqlite3.Cursor) -> str:
    return "{\"data\":{\"agenda_id\":" + str(cur.lastrowid) + "},\"op\":4}"

def getAgendaList(cur: sqlite3.Cursor) -> str:
    data = cur.fetchall()
    agendaList = []
    for agenda in data:
        agendaList.append(
            {
                "id": agenda[0],
                "name": agenda[1]
            }
        )

    m_json = {
        "data":{
            "agendaList": agendaList
        },
        "op": 4
    }
    return json.dumps(m_json)

def getPendingAgendaList(cur: sqlite3.Cursor) -> str:
    data = cur.fetchall()
    agendaList = []
    for agenda in data:
        agendaList.append(
            {
                "id": agenda[0],
                "name": agenda[1]
            }
        )

    m_json = {
        "data":{
            "agendaList": agendaList
        },
        "op": 4
    }
    return json.dumps(m_json)

def createEvent(cur: sqlite3.Cursor) -> str:
    return "{\"data\":{\"event_id\":" + str(cur.lastrowid) + "},\"op\":4}"

def getEventList(cur: sqlite3.Cursor) -> str:
    data = cur.fetchall()
    eventList = []
    for event in data:
        eventList.append(
            {
                "id": event[0],
                "name": event[1],
                "cancel": bool(event[2]),
                "start": event[3],
                "end": event[4],
                "color": event[5]
            }
        )

    m_json = {
        "data":{
            "eventList": eventList
        },
        "op": 4
    }
    return json.dumps(m_json)
