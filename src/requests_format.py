
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
                "desc": event[2],
                "cancel": bool(event[3]),
                "start": event[4],
                "end": event[5],
                "color": event[6]
            }
        )

    m_json = {
        "data":{
            "eventList": eventList
        },
        "op": 4
    }
    return json.dumps(m_json)
