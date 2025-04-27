from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem, QColor, QStandardItemModel
from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel, QDateEdit, QTimeEdit, QComboBox, QPushButton
#from DAO import



class EventMenu(QDialog):
    def __init__(self, mainpage , eventpage):
        super().__init__(parent=eventpage)

        self.ui = mainpage.ui

        self.layout = QVBoxLayout(self)

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
        self.agendas = [] #liste des agendas de l'utilisateur
        # TODO : voir quoi mettre dans ces dico
        self.repeat = {} #choix répétition
        self.reminder = {} #choix rappel

        self.ok_button = QPushButton()
        self.cancel_button = QPushButton()

        # Connection des widgets au layout
        self.layout.addWidget(self.event_name_label)
        self.layout.addWidget(self.event_name)
        self.layout.addWidget(self.event_location_label)
        self.layout.addWidget(self.event_location)
        self.layout.addWidget(self.date_event_label)
        self.layout.addWidget(self.date_event)
        self.layout.addWidget(self.time_event_label)
        self.layout.addWidget(self.time_event)
        self.layout.addWidget(self.color_event_label)
        self.layout.addWidget(self.color_event)
        self.layout.addWidget(self.agendas_label)
        self.layout.addWidget(self.agenda_event)

        model = QStandardItemModel()

        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # remplissage choix agenda


        # fenetre en francais
        if self.ui.current_lang == "fr":
            self.colors = {"Rouge": "#b41d1d",
                           "Orange": "#cd8423",
                           "Jaune": "#bfcd23",
                           "Vert": "#1c9d1c",
                           "Bleu": "#342aff",
                           "Violet": "#8723cd",
                           "Rose": "#cd2393"}  # choix couleur
            self.setWindowTitle("Créer un évenement")
            self.event_name_label.setText("Nom :")
            self.event_location_label.setText("Lieu :")
            self.date_event_label.setText("Date :")
            self.time_event_label.setText("Heure :")
            self.color_event_label.setText("Couleur :")

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
            self.setWindowTitle("Create event")
            self.event_name_label.setText("Name :")
            self.event_location_label.setText("Location :")
            self.date_event_label.setText("Date :")
            self.time_event_label.setText("Time :")
            self.color_event_label.setText("Color :")

            self.ok_button.setText("Ok")
            self.cancel_button.setText("Cancel")

        for name, hex_code in self.colors.items():
            item = QStandardItem(name)
            item.setBackground(QColor(hex_code))
            item.setForeground(Qt.GlobalColor.black)  # texte en noir pour une meilleure lisibilité
            model.appendRow(item)

        self.color_event.setModel(model)

        self.setLayout(self.layout)


    # recuperation des données entrée par l'utilisateur
    def get_data(self):
        '''
        Récupère les données de l'utilisateur sous forme de dictionnaire
        :return: Dictionnaire des données
        '''
        data_dic = {"name" : self.event_name.text(),
                    "location" : self.event_location.text(),
                    "date" : self.date_event.text(),
                    "time" : self.time_event.text(),
                    "color" : self.colors[self.color_event.currentText()]} #recupération du code ASCII de la couleur choisie
        return data_dic