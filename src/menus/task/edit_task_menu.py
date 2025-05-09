# Import bibliothèques
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QColor
from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel, QDateEdit, QTimeEdit, QPushButton, QComboBox, \
    QListWidgetItem
from datetime import datetime as dt

# Nos import
from src.menus.event.event_list_menu import EventListMenu

import src.DAO as DAO
from src.dataclass.event import Event


class EditTaskMenu(QDialog):
    def __init__(self, mainpage, eventpage: EventListMenu, item: QListWidgetItem):
        super().__init__(parent=eventpage)

        self.ui = mainpage.ui

        layout = QVBoxLayout(self)

        self.new_name_label = QLabel()  # nouveau nom
        self.new_name = QLineEdit()  # nouveau nom
        self.new_details_label = QLabel() # nouveaux détails
        self.new_details = QLineEdit() # nouveaux détails
        self.new_date_label = QLabel()  # nouvelle date
        self.new_date = QDateEdit()  # nouvelle date
        self.new_hour_label = QLabel()  # nouvelle heure
        self.new_hour = QTimeEdit()  # nouvelle heure
        self.new_color_label = QLabel()  # nouvelle couleur
        self.new_color = QComboBox()  # nouvelle couleur
        self.colors = {}  # dico couleurs

        self.ok_button = QPushButton()
        self.cancel_button = QPushButton()

        layout.addWidget(self.new_name_label)
        layout.addWidget(self.new_name)
        layout.addWidget(self.new_date_label)
        layout.addWidget(self.new_date)
        layout.addWidget(self.new_hour_label)
        layout.addWidget(self.new_hour)
        layout.addWidget(self.new_color_label)
        layout.addWidget(self.new_color)
        layout.addWidget(self.new_details_label)
        layout.addWidget(self.new_details)

        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        model_agenda = QStandardItemModel()
        model_color = QStandardItemModel()
        model_repeat = QStandardItemModel()
        model_reminder = QStandardItemModel()

        #self.event: Event = eventpage.get_event_selected(item)
        self.new_name.setText(self.event.name)

        # 1. Convertir en datetime standard Python
        #dt = datetime.fromtimestamp(self.event.start)

        # TODO Léo : mettre les infos courantes de la task
        #self.new_date.setDate(QDate(dt.year, dt.month, dt.day))
        #self.new_hour.setTime(QTime(dt.hour, dt.minute, dt.second))
        # self.new_details.setText()
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
            self.ok_button.setText("Valider")
            self.cancel_button.setText("Annuler")
            self.new_color_label.setText("Couleur")
            self.new_details_label.setText("Détails")

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
            self.ok_button.setText("Ok")
            self.cancel_button.setText("Cancel")
            self.new_color_label.setText("Color")
            self.new_details_label.setText("Details")

        for name, hex_code in self.colors.items():
            item = QStandardItem(name)
            item.setBackground(QColor(hex_code))
            item.setForeground(Qt.GlobalColor.black)  # texte en noir pour une meilleure lisibilité
            model_color.appendRow(item)
        self.new_color.setModel(model_color)

        self.setLayout(layout)

    def get_new_task(self):
        '''
        Récupération des nouvelles données entrées par l'utilisateurs et enregistrement dans la base de données
        :return: None
        '''
        # {'name': self.new_name.text(), 'date': self.new_date.text(), 'hour': self.new_hour.text(), 'location': self.new_location.text()}
        '''
        # TODO Léo réadapter la récupération de données pour intégrer les répétitions et rappels voir comment gérer modif
        timestamp = datetime.strptime(f"{self.new_date.text()} {self.new_hour.text()}", "%d/%m/%Y %H:%M").timestamp()
        return Event(
            id=self.event.id,
            name=self.new_name.text(),
            cancel=self.event.cancel,
            start=timestamp,
            end=timestamp + 3600  # Une heure après
        )'''
