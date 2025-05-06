
# Import bibliothèques
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QColor
from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel, QDateEdit, QTimeEdit, QPushButton, QComboBox, QListWidgetItem
from datetime import datetime

# Nos import
from .event_list_menu import EventListMenu

import src.DAO as DAO
from src.dataclass import Event

class EditEventMenu(QDialog) :
    def __init__(self, mainpage, eventpage: EventListMenu, item: QListWidgetItem):
        super().__init__(parent = eventpage)
        
        self.ui = mainpage.ui

        layout = QVBoxLayout(self)

        self.new_name_label = QLabel()  # nouveau nom
        self.new_name = QLineEdit()  # nouveau nom
        self.new_date_label = QLabel()  # nouvelle date
        self.new_date = QDateEdit()  # nouvelle date
        self.new_hour_label = QLabel()  # nouvelle heure
        self.new_hour = QTimeEdit()  # nouvelle heure
        self.new_location_label = QLabel()  # nouveau lieu
        self.new_location = QLineEdit()  # nouveau lieu
        self.new_color_label = QLabel() # nouvelle couleur
        self.new_color = QComboBox() #nouvelle couleur
        self.colors = {} #dico couleurs
        self.new_agenda_label = QLabel() # nouvel agenda
        self.new_agenda = QComboBox() # nouvel agenda
        self.new_repeat_label = QLabel()  # répétition
        self.repeat = {}  # choix répétition
        self.new_repeat_event = QComboBox()  # répétition
        self.new_reminder_label = QLabel()  # rappel
        self.reminder = {}  # choix rappel
        self.new_reminder_event = QComboBox()  # rappel

        self.ok_button = QPushButton()
        self.cancel_button = QPushButton()

        layout.addWidget(self.new_name_label)
        layout.addWidget(self.new_name)
        layout.addWidget(self.new_date_label)
        layout.addWidget(self.new_date)
        layout.addWidget(self.new_hour_label)
        layout.addWidget(self.new_hour)
        layout.addWidget(self.new_location_label)
        layout.addWidget(self.new_location)
        layout.addWidget(self.new_agenda_label)
        layout.addWidget(self.new_agenda)
        self.layout.addWidget(self.new_repeat_label)
        self.layout.addWidget(self.new_repeat_event)
        self.layout.addWidget(self.new_reminder_label)
        self.layout.addWidget(self.new_reminder_event)

        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        model_agenda = QStandardItemModel()
        model_color = QStandardItemModel()
        model_repeat = QStandardItemModel()
        model_reminder = QStandardItemModel()

        # remplissage choix agenda
        for agenda in DAO.agendalist:
            model_agenda.appendRow(QStandardItem(agenda.name))
        self.new_agenda.setModel(model_agenda)

        self.event: Event = eventpage.get_event_selected(item)
        self.new_name.setText(self.event.name)

        # 1. Convertir en datetime standard Python
        dt = datetime.fromtimestamp(self.event.start)

        self.new_date.setDate(QDate(dt.year, dt.month, dt.day))
        self.new_hour.setTime(QTime(dt.hour, dt.minute, dt.second))
        # self.new_location.setText()
        # self.new_agenda.setCurrentText()
        # self.new_color.setCurrentText()

        if self.ui.current_lang == 'fr':
            self.colors = {"Rouge": "#b41d1d",
                           "Orange": "#cd8423",
                           "Jaune": "#bfcd23",
                           "Vert": "#1c9d1c",
                           "Bleu": "#342aff",
                           "Violet": "#8723cd",
                           "Rose": "#cd2393"}  # choix couleur
            self.setWindowTitle("Modifier évenement")
            self.new_name_label.setText("Nom")
            self.new_date_label.setText("Date")
            self.new_hour_label.setText("Heure")
            self.new_location_label.setText("Lieu")
            self.ok_button.setText("Valider")
            self.cancel_button.setText("Annuler")
            self.new_color_label.setText("Couleur")
            self.new_agenda_label.setText("Agenda")
            self.new_reminder_event.setText("Rappel :")
            self.reminder = {"Aucun": 0, "1 jour avant": 1, "2 jours avant": 2, "3 jours avant": 3, "5 jours avant": 5,
                             "1 semaine avant": 7, "10 jours avant": 10, "2 semaines avant": 14, "3 semaines avant": 21,
                             "4 semaines avant": 28}
            self.new_repeat_label.setText("Répétition :")
            self.repeat = {"Aucun": 0, "Chaque jour": 1, "Chaque semaine": 7, "Chaque mois": 31,
                           "Chaque année": 365}  # TODO ajuster pour mois et année

        elif self.ui.current_lang == 'en':
            self.colors = {"Red": "#b41d1d",
                           "Orange": "#cd8423",
                           "Yellow": "#bfcd23",
                           "Gree,": "#1c9d1c",
                           "Blue": "#342aff",
                           "Purple": "#8723cd",
                           "Pink": "#cd2393"}  # choix couleur
            self.setWindowTitle("Edit event")
            self.new_name_label.setText("Name")
            self.new_date_label.setText("Date")
            self.new_hour_label.setText("Hour")
            self.new_location_label.setText("Location")
            self.ok_button.setText("Ok")
            self.cancel_button.setText("Cancel")
            self.new_color_label.setText("Color")
            self.new_agenda_label.setText("Diary")
            self.new_reminder_label.setText("Reminder :")
            self.reminder = {"None": 0, "1 day before": 1, "2 days before": 2, "3 days before": 3, "5 days before": 5,
                             "1 week before": 7, "10 days before": 10, "2 weeks before": 14, "3 weeks before": 21,
                             "4 weeks before": 28}
            self.new_repeat_label.setText("Repeat :")
            self.repeat = {"None": 0, "Every day": 1, "Every week": 7, "Every month": 31,
                           "Every year": 365}  # TODO ajuster pour mois et année

        for name, hex_code in self.colors.items():
            item = QStandardItem(name)
            item.setBackground(QColor(hex_code))
            item.setForeground(Qt.GlobalColor.black)  # texte en noir pour une meilleure lisibilité
            model_color.appendRow(item)
        self.new_color.setModel(model_color)

        # remplissage combobox répétitions
        for name in self.repeat.keys():
            item = QStandardItem(name)
            model_repeat.appendRow(item)
        self.new_repeat_event.setModel(model_repeat)

        # remplissage combobox rappels
        for name in self.reminder.keys():
            item = QStandardItem(name)
            model_reminder.appendRow(item)
        self.new_reminder_event.setModel(model_reminder)

        self.setLayout(layout)

    def get_new_event(self) -> Event:
        '''
        Récupération des nouvelles données entrées par l'utilisateurs et enregistrement dans la base de données
        :return: None
        '''
        # {'name': self.new_name.text(), 'date': self.new_date.text(), 'hour': self.new_hour.text(), 'location': self.new_location.text()}

        # TODO Léo réadapter la récupération de données pour intégrer les répétitions et rappels voir comment gérer modif
        timestamp = datetime.strptime(f"{self.new_date.text()} {self.new_hour.text()}", "%m/%d/%y %I:%M %p").timestamp()
        return Event(
            id=self.event.id,
            name=self.new_name.text(),
            cancel=self.event.cancel,
            start=timestamp,
            end=timestamp + 3600 # Une heure après
        )
        