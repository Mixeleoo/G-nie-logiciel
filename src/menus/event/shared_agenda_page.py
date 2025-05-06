from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate, QPoint, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QMenu, QListWidgetItem
from datetime import datetime
import src.DAO as DAO
from src.dataclass.event import Event


class SharedAgendaMenu(QDialog):
    def __init__(self, mainpage , eventpage):
        super().__init__(parent=eventpage)

        self.ui = mainpage.ui
        self.mainpage = mainpage
        self.cancel_font = QFont()
        self.cancel_font.setStrikeOut(True)

        try:

            self.layout = QVBoxLayout(self)

            self.shared_list = QtWidgets.QListWidget(self) # liste des agenda partagé en attente d'acceptation

            #TODO Léo : adapter la boucle pour récupérer les agendas partagés à l'utilisateur
            '''for agenda in DAO.agendalist:
                event_list = DAO.eventdao.get_list(agenda)
                for e in event_list:
                    # 1. Convertir curr_date (QDate) en datetime
                    curr_timestamp = datetime(
                        curr_date.year(),
                        curr_date.month(),
                        curr_date.day()
                    ).timestamp()
                    dt = datetime.fromtimestamp(e.start).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()

                    if curr_timestamp == dt:
                        self.event_listleo.append(e)
                        item = QtWidgets.QListWidgetItem(e.name)
                        if e.cancel:
                            item.setFont(self.cancel_font)
                        self.event_list.addItem(item)'''

            self.layout.addWidget(self.shared_list)

            self.setLayout(self.layout)

            self.shared_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.shared_list.customContextMenuRequested.connect(self.show_shared_menu)
        except Exception as e:
            raise e

    def get_event_selected(self, item: QListWidgetItem) -> Event:
        return self.event_listleo[self.event_list.row(item)]

    def show_shared_menu(self, pos: QPoint):
        a_lang = {'fr' : ['Accepter','Refuser'],
                'en' : ['Accept', 'Deny']}

        item = self.shared_list.itemAt(pos)
        if item:
            menu = QMenu()

            accepter_action = menu.addAction(a_lang[self.ui.current_lang][0])
            refuser_action = menu.addAction(a_lang[self.ui.current_lang][1])

            action = menu.exec(self.event_list.mapToGlobal(pos))

            # gestion modification de l'évenement
            if action == accepter_action:
                self.accept_agenda(item)
            elif action == refuser_action:
                self.deny_agenda(item)

    def accept_agenda(self,item : QListWidgetItem):
        '''
        Ajoute l'agenda accepté dans la liste des agenda de l'utilisateur
        :return: None
        '''
        #TODO Léo : gérer l'ajout

        self.shared_list.remove(item)

    def deny_agenda(self, item : QListWidgetItem):
        '''
        Refuse l'agenda partagé et le supprime des agenda en attente
        :return: None
        '''
        #TODO Léo : gérer supression de shared dans la bd

        self.shared_list.remove(item)
