
from dataclasses import field, Field
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem, QColor, QStandardItemModel
from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel, QDateEdit, QTimeEdit, QComboBox, QPushButton

import src.DAO as DAO
from src.dataclass.event import Event, Color

def hexcolor_to_int(hexcolor: str) -> Color:
    hexcolor = hexcolor.lstrip('#')
    return Color(r=int(hexcolor[0:2], 16), g=int(hexcolor[2:4], 16), b=int(hexcolor[4:6], 16))

def get_day_of_week(date_str):
    # Convertir la chaîne de caractères en objet datetime
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    
    # Récupérer le jour de la semaine sous forme de numéro : 0= lundi, 6= dimanche
    day_num = date_obj.weekday() + 1  # on ajoute 1 pour que 1= lundi, 7= dimanche
    return day_num

class EventMenuABC(QDialog):
    def __init__(self, mainpage, eventpage):
        '''
        Intialisation de la page de paramètrage d'un événement
        '''
        super().__init__(parent=eventpage)

        self.ui = mainpage.ui

        self.event_name_label = QLabel() #nom
        self.event_name = QLineEdit() #nom
        self.event_location_label = QLabel() #lieu
        self.event_location = QLineEdit() #lieu
        self.date_event_label = QLabel() #date
        self.date_event = QDateEdit() #date
        self.time_event_label = QLabel() #heure
        self.time_event = QTimeEdit() #heure
        self.color_event_label = QLabel() #couleur
        self.color_event = QComboBox() #couleur
        self.colors = {} #choix couleur
        self.agendas_label = QLabel() # agenda
        self.agenda_event = QComboBox() # agenda
        self.repeat_label = QLabel() #répétition
        self.repeat = {} #choix répétition
        self.repeat_event = QComboBox()  #répétition
        self.reminder_label = QLabel() #rappel
        self.reminder = {} #choix rappel
        self.reminder_event = QComboBox() #rappel

        layout = QVBoxLayout(self)

        self.ok_button = QPushButton()
        self.cancel_button = QPushButton()

        # Connection des widgets au layout
        layout.addWidget(self.event_name_label)
        layout.addWidget(self.event_name)
        layout.addWidget(self.event_location_label)
        layout.addWidget(self.event_location)
        layout.addWidget(self.date_event_label)
        layout.addWidget(self.date_event)
        layout.addWidget(self.time_event_label)
        layout.addWidget(self.time_event)
        layout.addWidget(self.color_event_label)
        layout.addWidget(self.color_event)
        layout.addWidget(self.agendas_label)
        layout.addWidget(self.agenda_event)
        layout.addWidget(self.repeat_label)
        layout.addWidget(self.repeat_event)
        layout.addWidget(self.reminder_label)
        layout.addWidget(self.reminder_event)

        model_color = QStandardItemModel()
        model_agenda = QStandardItemModel()
        model_repeat = QStandardItemModel()
        model_reminder = QStandardItemModel()

        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        # remplissage choix agenda
        for agenda in DAO.agendalist:
            item = QStandardItem(agenda.name)
            model_agenda.appendRow(item)
        self.agenda_event.setModel(model_agenda)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
            
        # fenetre en francais
        if self.ui.current_lang == "fr":
            self.colors = {
                "Rouge": "#b41d1d",
                "Orange": "#cd8423",
                "Jaune": "#bfcd23",
                "Vert": "#1c9d1c",
                "Bleu": "#342aff",
                "Violet": "#8723cd",
                "Rose": "#cd2393"
            }  # choix couleur
            
            self.event_name_label.setText("Nom :")
            self.event_location_label.setText("Lieu :")
            self.date_event_label.setText("Date :")
            self.time_event_label.setText("Heure :")
            self.color_event_label.setText("Couleur :")
            self.agendas_label.setText("Agenda :")
            self.reminder_label.setText("Rappel :")
            self.reminder = {
                "Aucun" : 0,
                "1 jour avant" : 1,
                "2 jours avant" : 2,
                "3 jours avant" : 3,
                "5 jours avant" : 5,
                "1 semaine avant" : 7,
                "10 jours avant" : 10,
                "2 semaines avant" : 14,
                "3 semaines avant" : 21,
                "4 semaines avant" : 28
            }
            self.repeat_label.setText("Répétition :")
            self.repeat: dict[str, Field] = {
                "Aucun" : field(default_factory=lambda: Event(id=0)),
                "Chaque jour": field(default_factory=lambda: Event(frequency='daily', interval=1)),
                "Chaque semaine": field(default_factory=lambda: Event(frequency='weekly', interval=1, by_day=get_day_of_week(self.date_event.text()))),
                "Chaque mois": field(default_factory=lambda: Event(frequency='monthly', interval=1, by_month_day=self.date_event.text().split("/")[1])),
                "Chaque année": field(default_factory=lambda: Event(frequency='yearly', interval=1, by_day=self.date_event.text().split("/")[0], by_month_day=self.date_event.text().split("/")[1]))
            }

            self.ok_button.setText("Valider")
            self.cancel_button.setText("Annuler")

        # fenetre en anglais
        elif self.ui.current_lang == "en":
            self.colors = {"Red": "#b41d1d",
                           "Orange": "#cd8423",
                           "Yellow": "#bfcd23",
                           "Gree,": "#1c9d1c",
                           "Blue": "#342aff",
                           "Purple": "#8723cd",
                           "Pink": "#cd2393"}  # choix couleur
            
            self.event_name_label.setText("Name :")
            self.event_location_label.setText("Location :")
            self.date_event_label.setText("Date :")
            self.time_event_label.setText("Time :")
            self.color_event_label.setText("Color :")
            self.agendas_label.setText("Diary :")
            self.reminder_label.setText("Reminder :")
            self.reminder = {
                "None" : 0,
                "1 day before": 1,
                "2 days before": 2,
                "3 days before": 3,
                "5 days before": 5,
                "1 week before": 7,
                "10 days before": 10,
                "2 weeks before": 14,
                "3 weeks before": 21,
                "4 weeks before": 28
            }
            self.repeat_label.setText("Repeat :")
            self.repeat: dict[str, Field] = {
                "None" : field(default_factory=lambda: Event(id=0)),
                "Every day": field(default_factory=lambda: Event(frequency='daily', interval=1)),
                "Every week": field(default_factory=lambda: Event(frequency='weekly', interval=1, by_day=get_day_of_week(self.date_event.text()))),
                "Every month": field(default_factory=lambda: Event(frequency='monthly', interval=1, by_month_day=self.date_event.text().split("/")[1])),
                "Every year": field(default_factory=lambda: Event(frequency='yearly', interval=1, by_day=self.date_event.text().split("/")[0], by_month_day=self.date_event.text().split("/")[1]))
            }

            self.ok_button.setText("Ok")
            self.cancel_button.setText("Cancel")

        # remplissage combobox couleurs
        for name, hex_code in self.colors.items():
            item = QStandardItem(name)
            item.setBackground(QColor(hex_code))
            item.setForeground(Qt.GlobalColor.black)  # texte en noir pour une meilleure lisibilité
            model_color.appendRow(item)
        self.color_event.setModel(model_color)

        # remplissage combobox répétitions
        for name in self.repeat.keys():
            item = QStandardItem(name)
            model_repeat.appendRow(item)
        self.repeat_event.setModel(model_repeat)

        # remplissage combobox rappels
        for name in self.reminder.keys():
            item = QStandardItem(name)
            model_reminder.appendRow(item)
        self.reminder_event.setModel(model_reminder)

        self.setLayout(layout)

    @property
    def current_repeat(self) -> Event:
        '''
        Retourne la récurrence actuelle de l'événement
        :return: La récurrence actuelle
        '''
        return self.repeat[self.repeat_event.currentText()].default_factory()
    
    @property
    def current_color(self) -> Color:
        '''
        Retourne la couleur actuelle de l'événement
        :return: La couleur actuelle
        '''
        return hexcolor_to_int(self.colors[self.color_event.currentText()])

    # recuperation des données entrée par l'utilisateur
    def get_data(self) -> Event:
        '''
        Récupère les données de l'utilisateur sous forme de dictionnaire
        :return: Le nouvel evenement créé
        '''
        #TODO Léo réadapter la récupération de données pour intégrer les rappels
        timestamp = int(
            datetime.strptime(f"{self.date_event.text()} {self.time_event.text()}", "%d/%m/%Y %H:%M").timestamp())

        current_repeat = self.current_repeat

        return Event(
            id=self.agenda_event.currentIndex(),
            name=self.event_name.text(),
            start=timestamp,
            end=timestamp + 3600, # Une heure plus tard
            color=self.current_color,
            frequency=current_repeat.frequency,
            interval=current_repeat.interval,
            by_day=current_repeat.by_day,
            by_month_day=current_repeat.by_month_day,
            until=current_repeat.until
        )
