from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem, QColor, QStandardItemModel
from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel, QDateEdit, QTimeEdit, QComboBox, QPushButton
from dataclass import Task, Color
import datetime


def hexcolor_to_int(hexcolor: str) -> Color:
    hexcolor = hexcolor.lstrip('#')
    return Color(r=int(hexcolor[0:2], 16), g=int(hexcolor[2:4], 16), b=int(hexcolor[4:6], 16))

class TaskMenu(QDialog):
    def __init__(self, mainpage , taskpage):
        super().__init__(parent=taskpage)

        self.ui = mainpage.ui

        self.layout = QVBoxLayout(self)
        self.task_name_label = QLabel() #nom
        self.task_name = QLineEdit() #nom
        self.task_details_label = QLabel() #detail
        self.date_task_label = QLabel() #date
        self.task_details = QLineEdit()  # detail
        self.date_task = QDateEdit() #date
        self.time_task_label = QLabel() #heure
        self.time_task = QTimeEdit() #heure
        self.color_task_label = QLabel() #couleur
        self.color_task = QComboBox() #couleur
        self.colors = {} #choix couleur
        #TODO : voir quoi mettre dans ces dico
        self.repeat = {}  # choix répétition
        self.reminder = {}  # choix rappel

        self.ok_button = QPushButton()
        self.cancel_button = QPushButton()

        # Connection des widgets au layout
        self.layout.addWidget(self.task_name_label)
        self.layout.addWidget(self.task_name)
        self.layout.addWidget(self.task_details_label)
        self.layout.addWidget(self.task_details)
        self.layout.addWidget(self.date_task_label)
        self.layout.addWidget(self.date_task)
        self.layout.addWidget(self.time_task_label)
        self.layout.addWidget(self.time_task)
        self.layout.addWidget(self.color_task_label)
        self.layout.addWidget(self.color_task)

        model = QStandardItemModel()

        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # fenetre en francais
        if self.ui.current_lang == "fr":
            self.colors = {"Rouge": "#b41d1d",
                           "Orange": "#cd8423",
                           "Jaune": "#bfcd23",
                           "Vert": "#1c9d1c",
                           "Bleu": "#342aff",
                           "Violet": "#8723cd",
                           "Rose": "#cd2393"}  # choix couleur
            self.setWindowTitle("Créer une tâche")
            self.task_name_label.setText("Nom :")
            self.task_details_label.setText("Détails :")
            self.date_task_label.setText("Date :")
            self.time_task_label.setText("Heure :")
            self.color_task_label.setText("Couleur :")

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
            self.setWindowTitle("Create task")
            self.task_name_label.setText("Name :")
            self.task_details_label.setText("Details :")
            self.date_task_label.setText("Date :")
            self.time_task_label.setText("Time :")
            self.color_task_label.setText("Color :")

            self.ok_button.setText("Ok")
            self.cancel_button.setText("Cancel")

        for name, hex_code in self.colors.items():
            item = QStandardItem(name)
            item.setBackground(QColor(hex_code))
            item.setForeground(Qt.GlobalColor.black)  # texte en noir pour une meilleure lisibilité
            model.appendRow(item)

        self.color_task.setModel(model)

        self.setLayout(self.layout)

    # recuperation des données entrée par l'utilisateur
    def get_data(self) -> Task:
        '''
        Récupère les données de l'utilisateur sous forme de dictionnaire
        :return: Dictionnaire des données
        '''

        timestamp = datetime.strptime(f"{self.date_task.text()} {self.time_task.text()}", "%m/%d/%y %I:%M %p").timestamp()
        
        return Task(
            name=self.task_name.text(),
            details=self.task_details.text(),
            date=timestamp,
            color=hexcolor_to_int(self.colors[self.color_event.currentText()])
        )