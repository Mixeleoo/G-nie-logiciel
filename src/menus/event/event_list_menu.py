from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate, QPoint, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QMessageBox, QMenu, QLineEdit, QLabel, \
    QPushButton, QListWidgetItem
from menus.event.edit_event_menu import EditEventMenu
from menus.event.rename_event_menu import RenameEventMenu

from datetime import datetime
import DAO
from dataclass import Event


class EventListMenu(QDialog):
    def __init__(self, mainpage , eventpage, curr_date : QDate):
        super().__init__(parent=eventpage)

        self.ui = mainpage.ui
        self.mainpage = mainpage
        self.cancel_font = QFont()
        self.cancel_font.setStrikeOut(True)

        if self.ui.current_lang == 'fr' :
            self.setWindowTitle(f"Evenement(s) du {curr_date.toString('dd/MM/yyyy')}")
        elif self.ui.current_lang == 'en' :
            self.setWindowTitle(f"{curr_date.toString('dd/MM/yyyy')} event(s)")

        self.layout = QVBoxLayout(self)

        self.event_list = QtWidgets.QListWidget(self) # liste des evenement à la date cliquée par l'utilisateur
        self.event_listleo: list[Event] = []

        for agenda in DAO.agendalist:
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
                    if e.cancel == True:
                        item.setFont(self.cancel_font)
                    self.event_list.addItem(item)

        self.layout.addWidget(self.event_list)

        self.setLayout(self.layout)

        self.event_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.event_list.customContextMenuRequested.connect(self.show_event_menu)


    def show_event_menu(self, pos : QPoint):
        a_lang = {'fr' : ['Modifier évenement','Renommer évenement', 'Annuler évenement', 'Supprimer évenement',"Ajouter à un agenda"],
                'en' : ['Edit event', 'Rename event', 'Cancel event', 'Delete event',"Add to diary"]}
        try :
            item = self.event_list.itemAt(pos)
            if item:
                menu = QMenu()

                modifier_action = menu.addAction(a_lang[self.ui.current_lang][0])
                add_to_diary_action = menu.addAction(a_lang[self.ui.current_lang][4])
                renommer_action = menu.addAction(a_lang[self.ui.current_lang][1])
                annuler_action = menu.addAction(a_lang[self.ui.current_lang][2])
                supprimer_action = menu.addAction(a_lang[self.ui.current_lang][3])

                action = menu.exec(self.event_list.mapToGlobal(pos))

                # gestion modification de l'évenement
                if action == modifier_action:
                    self.edit_event()
                elif action == renommer_action:
                    self.rename_event()
                elif action == supprimer_action:
                    self.delete_event()
                elif action == annuler_action:
                    self.cancel_event(item) # Vachement brut-force le truc
                elif action == add_to_diary_action:
                    self.add_event_to_diary()

        except Exception as e :
            print(f"Erreur dans show_event_menu: {e}")

    def rename_event(self):
        '''
        Crée et ouvre une fenêtre pour permettre à l'utilisateur de renommer l'évenement choisi
        :return:
        '''
        rename_page = RenameEventMenu(self.mainpage, self)
        if rename_page.exec() :
            print(rename_page.get_new_data())


    def edit_event(self):
        '''
        Crée et ouvre une page d'édition pour permettre la modification de l'évenement choisi à l'utilisateur
        :return: None
        '''
        #TODO : voir comment mettre les infos modifiable de l'event dans les editline + comment récupérer les infos modifiée
        edit_page = EditEventMenu(self.mainpage,self)
        if edit_page.exec() :
            print(edit_page.get_new_data())

    def delete_event(self):
        '''
        Supprime completement l'évenement de la base de données
        :return: None
        '''
        #TODO : voir comment supprimer un evenment
        print("event supp")

    def cancel_event(self, item: QListWidgetItem):
        '''
        Concerve l'évenement mais l'affiche barré dans la liste d'évenement
        :return: None
        '''
        DAO.eventdao.cancel(self.event_listleo[self.event_list.row(item)])
        item.setFont(self.cancel_font)
        print("évenement annulé")

    def add_event_to_diary(self):
        '''
        Crée et ouvre une liste des agenda disponibles pour permettre l'ajout dans l'une d'elle à l'utilisateur
        :return: None
        '''
        print('ajout agenda')
