
import json
from DAO import UserDAO, User, AgendaDAO, Agenda, EventDAO, Event
from dbcom import DBCom

HOST = '127.0.0.1'  # Adresse du serveur
PORT = 65439       # Port du serveur

if __name__ == "__main__":
    dbcom = DBCom(HOST, PORT)
    print("Connecté au serveur.")

    user = User(-1, "", "")
    userdao = UserDAO(dbcom)
    agendadao = AgendaDAO(dbcom)
    eventdao = EventDAO(dbcom)

    agendaList: list[Agenda] = []

    while True:
        message = input("Message à envoyer : ")
        message = message.split(' ')

        # REGISTER
        if message[0] == 'register':
            user.mail = message[1]
            user.mdp = message[2]
            recu = userdao.insert(user)

        # CONNECT
        elif message[0] == 'connect':
            user.mail = message[1]
            user.mdp = message[2]
            recu = user = userdao.connect(user)

        #                                              AGENDA

        # CREATE AGENDA
        elif message[0] == 'cra':
            if user.id == -1:
                print("Vous n'êtes toujours pas connectés !")
                continue

            agendadao.insert(user, Agenda(name=message[1]))

        # SET AGENDA NAME
        elif message[0] == 'san':
            if user.id == -1:
                print("Vous n'êtes toujours pas connectés !")
                continue

            agendadao.update(Agenda(1, "modifié"))

        # getAgendaList
        elif message[0] == 'gal':
            if user.id == -1:
                print("Vous n'êtes toujours pas connectés !")
                continue

            agendaList = agendadao.get_list(user)
            print(agendaList)

        #                                               EVENT

        # getEventList
        elif message[0] == 'gel':
            if user.id == -1:
                print("Vous n'êtes toujours pas connectés !")
                continue
            
            if agendaList == []:
                print("Stp fais un ptit gal comme ça jpeux récupérer les event du premier agenda récupéré")
                continue

            print(eventdao.get_list(agendaList[0]))

        # CREATE EVENT
        elif message[0] == 'cre':
            if user.id == -1:
                print("Vous n'êtes toujours pas connectés !")
                continue
            
            if agendaList == []:
                print("Stp fais un ptit gal comme ça jpeux récupérer les event du premier agenda récupéré")
                continue

            eventdao.insert(agendaList[0], Event(name=message[1]))

        # SET EVENT NAME
        elif message[0] == 'sen':
            if user.id == -1:
                print("Vous n'êtes toujours pas connectés !")
                continue

            eventdao.update(Event(1, "modifié"))
