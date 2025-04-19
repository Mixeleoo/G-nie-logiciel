from PyQt6.QtCore import QDate, Qt, QPoint
from PyQt6.QtWidgets import QWidget, QMenu, QInputDialog, QMessageBox, QDialog, QLineEdit, QVBoxLayout, QLabel, \
    QPushButton, QDateEdit, QTimeEdit


#from src.main import MainWindow
#from pages.event_page import EventPage



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

        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)

        # fenetre en francais
        if self.ui.current_lang == "fr":
            self.setWindowTitle("Créer un évenement")
            self.event_name_label.setText("Nom :")
            self.event_location_label.setText("Lieu :")
            self.date_event_label.setText("Date :")
            self.time_event_label.setText("Heure :")

            self.ok_button.setText("Valider")
            self.cancel_button.setText("Annuler")

        # fenetre en anglais
        elif self.ui.current_lang == "en":
            self.setWindowTitle("Create event")
            self.event_name_label.setText("Name :")
            self.event_location_label.setText("Location :")
            self.date_event_label.setText("Date :")
            self.time_event_label.setText("Time :")

            self.ok_button.setText("Ok")
            self.cancel_button.setText("Cancel")

        self.setLayout(self.layout)


    # recuperation des données entrée par l'utilisateur
    def get_data(self):
        '''
        Récupère les données de l'utilisateur sous forme de dictionnaire
        :return: Dictionnaire des données
        '''
        data_dic = {"name" : self.event_name.text(), "location" : self.event_location.text(), "date" : self.date_event.text(), "time" : self.time_event.text() }
        return data_dic