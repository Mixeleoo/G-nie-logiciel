from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate, QPoint, Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QMenu, QListWidgetItem
import src.DAO as DAO
from DAO import pendingsharedagendalist
from src.dataclass.agenda import Agenda


class SharedAgendaMenu(QDialog):
    def __init__(self, mainpage , eventpage):
        super().__init__(parent=eventpage)

        self.ui = mainpage.ui
        self.mainpage = mainpage
        trans_dic = {"en" : "Shared diary", "fr" : "Agenda partagés"}

        self.setWindowTitle(trans_dic[self.ui.current_lang])

        self.layout = QVBoxLayout(self)
        self.shared_list = QtWidgets.QListWidget(self) # liste des agenda partagé en attente d'acceptation
        self.shared_listleo: list[Agenda] = []

        for agenda in DAO.pendingsharedagendalist:
            self.shared_listleo.append(agenda)
            self.shared_list.addItem(
                QtWidgets.QListWidgetItem(agenda.name)
            )

        self.layout.addWidget(self.shared_list)

        self.setLayout(self.layout)

        self.shared_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.shared_list.customContextMenuRequested.connect(self.show_shared_menu)

    def show_shared_menu(self, pos: QPoint):
        print(pendingsharedagendalist)
        a_lang = {'fr' : ['Accepter','Refuser'],
                'en' : ['Accept', 'Deny']}

        item = self.shared_list.itemAt(pos)
        if item:
            menu = QMenu()

            accepter_action = menu.addAction(a_lang[self.ui.current_lang][0])
            refuser_action = menu.addAction(a_lang[self.ui.current_lang][1])

            action = menu.exec(self.shared_list.mapToGlobal(pos))

            # On supprime l'agenda dans la liste
            print(pendingsharedagendalist)
            DAO.pendingsharedagendalist.remove(self.selected_agenda)
            print(pendingsharedagendalist)

            # gestion modification de l'évenement
            if action == accepter_action:
                self.accept_agenda(item)
            elif action == refuser_action:
                self.deny_agenda(item)

            # Dans tous les cas on supprime l'agenda des choix visuels
            self.shared_list.takeItem(self.shared_list.row(item))

    @property
    def selected_agenda(self) -> Agenda:
        '''
        Retourne l'agenda sélectionné
        :return: Agenda
        '''
        return self.shared_listleo[self.shared_list.currentIndex().row()]

    def accept_agenda(self,item : QListWidgetItem):
        '''
        Ajoute l'agenda accepté dans la liste des agenda de l'utilisateur
        :return: None
        '''
        DAO.agendadao.accept_shared_agenda(
            DAO.user, self.selected_agenda
        )

    def deny_agenda(self, item : QListWidgetItem):
        '''
        Refuse l'agenda partagé et le supprime des agenda en attente
        :return: None
        '''
        DAO.agendadao.deny_shared_agenda(
            DAO.user, self.selected_agenda
        )
