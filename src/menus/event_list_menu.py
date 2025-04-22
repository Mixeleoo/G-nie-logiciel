from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate, QPoint, Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QMessageBox, QMenu, QLineEdit, QDateEdit, QTimeEdit, QLabel, \
    QPushButton

from src.data_test.list_data_test import *


class EventListMenu(QDialog):
    def __init__(self, mainpage , eventpage, curr_date : QDate):
        super().__init__(parent=eventpage)

        self.ui = mainpage.ui

        if self.ui.current_lang == 'fr' :
            self.setWindowTitle(f"Evenement(s) du {curr_date.toString('dd/MM/yyyy')}")
        elif self.ui.current_lang == 'en' :
            self.setWindowTitle(f"{curr_date.toString('dd/MM/yyyy')} event(s)")

        self.layout = QVBoxLayout(self)

        self.event_list = QtWidgets.QListWidget(self) # liste des evenement à la date cliquée par l'utilisateur
        # TODO Léo : adpater la boucle au parcours de la base de données
        for e in event:
            if e['date'] == curr_date.toString('dd/MM/yyyy'):
                self.event_list.addItem(e['name'])


        self.layout.addWidget(self.event_list)

        self.setLayout(self.layout)

        self.event_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.event_list.customContextMenuRequested.connect(self.show_event_menu)


    def show_event_menu(self, pos : QPoint):
        a_lang = {'fr' : ['Modifier évenement','Renommer évenement', 'Annuler évenement', 'Supprimer évenement' , 8],
                'en' : ['Edit event', 'Rename event', 'Cancel event', 'Delete event', 5]}
        try :
            item = self.event_list.itemAt(pos)
            if item:
                menu = QMenu()

                modifier_action = menu.addAction(a_lang[self.ui.current_lang][0])
                renommer_action = menu.addAction(a_lang[self.ui.current_lang][1])
                annuler_action = menu.addAction(a_lang[self.ui.current_lang][2])
                supprimer_action = menu.addAction(a_lang[self.ui.current_lang][3])

                action = menu.exec(self.event_list.mapToGlobal(pos))

                # gestion modification de l'évenement
                if action == modifier_action:
                    self.edit_event(item.text())
                    #QMessageBox.information(self, "Action", f"{a_lang[self.ui.current_lang][0]} {item.text()}")
                elif action == renommer_action:
                    QMessageBox.information(self, "Action", f"{a_lang[self.ui.current_lang][1]} {item.text()}")
                elif action == supprimer_action:
                    QMessageBox.information(self, "Action", f"{a_lang[self.ui.current_lang][2]} {item.text()}")
                elif action == annuler_action:
                    QMessageBox.information(self, "Action", f"{a_lang[self.ui.current_lang][3]} {item.text()}")

        except Exception as e :
            print(f"Erreur dans show_event_menu: {e}")


    def edit_event(self, test_nom : str):
        edit_page = QDialog(self)
        layout = QVBoxLayout(edit_page)

        new_name_label = QLabel()  # nouveau nom
        new_name = QLineEdit() #nouveau nom
        new_date_label = QLabel() #nouvelle date
        new_date = QDateEdit() #nouvelle date
        new_hour_label = QLabel() #nouvelle heure
        new_hour = QTimeEdit() #nouvelle heure
        new_location_label = QLabel() #nouveau lieu
        new_location = QLineEdit() #nouveau lieu

        ok_button = QPushButton()
        cancel_button = QPushButton()

        layout.addWidget(new_name_label)
        layout.addWidget(new_name)
        layout.addWidget(new_date_label)
        layout.addWidget(new_date)
        layout.addWidget(new_hour_label)
        layout.addWidget(new_hour)
        layout.addWidget(new_location_label)
        layout.addWidget(new_location)

        # TODO : mettre les information courantes dans les editline
        new_name.setText(test_nom)
        # new_date.setDate()
        # new_hour.setTime()
        # new_location.setText()

        if self.ui.current_lang == 'fr' :
            new_name_label.setText("Nom")
            new_date_label.setText("Date")
            new_hour_label.setText("Heure")
            new_location_label.setText("Lieu")

        elif self.ui.current_lang == 'en' :
            new_name_label.setText("Name")
            new_date_label.setText("Date")
            new_hour_label.setText("Hour")
            new_location_label.setText("Location")

        edit_page.setLayout(layout)
        edit_page.exec()
