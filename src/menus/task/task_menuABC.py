from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QColor
from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel, QDateEdit, QTimeEdit, QPushButton, QComboBox
from datetime import datetime

# Nos import

from src.dataclass.color import Color
from src.dataclass.task import Task

def hexcolor_to_int(hexcolor: str) -> Color:
    hexcolor = hexcolor.lstrip('#')
    return Color(r=int(hexcolor[0:2], 16), g=int(hexcolor[2:4], 16), b=int(hexcolor[4:6], 16))


class TaskMenuABC(QDialog):
    def __init__(self, mainpage, taskpage):
        super().__init__(parent=taskpage)

        self.ui = mainpage.ui

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

        self.ok_button = QPushButton()
        self.cancel_button = QPushButton()

        layout = QVBoxLayout(self)

        layout.addWidget(self.task_name_label)
        layout.addWidget(self.task_name)
        layout.addWidget(self.task_details_label)
        layout.addWidget(self.task_details)
        layout.addWidget(self.date_task_label)
        layout.addWidget(self.date_task)
        layout.addWidget(self.time_task_label)
        layout.addWidget(self.time_task)
        layout.addWidget(self.color_task_label)
        layout.addWidget(self.color_task)

        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        model_color = QStandardItemModel()

        if self.ui.current_lang == 'fr':
            self.colors = {
                "Rouge": "#b41d1d",
                "Orange": "#cd8423",
                "Jaune": "#bfcd23",
                "Vert": "#1c9d1c",
                "Bleu": "#342aff",
                "Violet": "#8723cd",
                "Rose": "#cd2393"
            }  # choix couleur
            self.task_name_label.setText("Nom")
            self.date_task_label.setText("Date")
            self.time_task_label.setText("Heure")
            self.ok_button.setText("Valider")
            self.cancel_button.setText("Annuler")
            self.color_task_label.setText("Couleur")
            self.task_details_label.setText("Détails")

            self.ok_button.setText("Valider")
            self.cancel_button.setText("Annuler")

        elif self.ui.current_lang == 'en':
            self.colors = {
                "Red": "#b41d1d",
                "Orange": "#cd8423",
                "Yellow": "#bfcd23",
                "Green": "#1c9d1c",
                "Blue": "#342aff",
                "Purple": "#8723cd",
                "Pink": "#cd2393"
            }  # choix couleur
            self.task_name_label.setText("Name")
            self.date_task_label.setText("Date")
            self.time_task_label.setText("Hour")
            self.ok_button.setText("Ok")
            self.cancel_button.setText("Cancel")
            self.color_task_label.setText("Color")
            self.task_details_label.setText("Details")

            self.ok_button.setText("Ok")
            self.cancel_button.setText("Cancel")

        for name, hex_code in self.colors.items():
            item_c = QStandardItem(name)
            item_c.setBackground(QColor(hex_code))
            item_c.setForeground(Qt.GlobalColor.black)  # texte en noir pour une meilleure lisibilité
            model_color.appendRow(item_c)
        self.color_task.setModel(model_color)

        self.setLayout(layout)

    # recuperation des données entrée par l'utilisateur
    def get_data(self) -> Task:
        '''
        Récupère les données modifées
        :return: Task
        '''

        timestamp = int(datetime.strptime(f"{self.date_task.text()} {self.time_task.text()}", "%d/%m/%Y %H:%M").timestamp())
        
        return Task(
            name=self.task_name.text(),
            details=self.task_details.text(),
            date=timestamp,
            color=hexcolor_to_int(self.colors[self.color_task.currentText()])
        )
