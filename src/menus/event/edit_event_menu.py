from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QColor
from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel, QDateEdit, QTimeEdit, QPushButton, QComboBox
from DAO import agendalist


class EditEventMenu(QDialog) :
    def __init__(self, mainpage, eventpage):
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

        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        model_agenda = QStandardItemModel()
        model_color = QStandardItemModel()

        # remplissage choix agenda
        for agenda in agendalist:
            item = QStandardItem(agenda.name)
            model_agenda.appendRow(item)
        self.new_agenda.setModel(model_agenda)

        #TODO Léo : mettre les bons textes dans les edit line et combobox
        # self.new_name.setText()
        # self.new_date.setDate()
        # self.new_hour.setTime()
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

        for name, hex_code in self.colors.items():
            item = QStandardItem(name)
            item.setBackground(QColor(hex_code))
            item.setForeground(Qt.GlobalColor.black)  # texte en noir pour une meilleure lisibilité
            model_color.appendRow(item)
        self.new_color.setModel(model_color)

        self.setLayout(layout)

    def get_new_data(self):
        data_dic = {'name': self.new_name.text(), 'date': self.new_date.text(), 'hour': self.new_hour.text(), 'location': self.new_location.text()}
        return data_dic
        