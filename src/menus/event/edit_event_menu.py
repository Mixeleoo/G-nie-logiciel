from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel, QDateEdit, QTimeEdit, QPushButton


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

        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # self.new_name.setText()
        # self.new_date.setDate()
        # self.new_hour.setTime()
        # self.new_location.setText()

        if self.ui.current_lang == 'fr':
            self.setWindowTitle("Modifier évenement")
            self.new_name_label.setText("Nom")
            self.new_date_label.setText("Date")
            self.new_hour_label.setText("Heure")
            self.new_location_label.setText("Lieu")
            self.ok_button.setText("Valider")
            self.cancel_button.setText("Annuler")

        elif self.ui.current_lang == 'en':
            self.setWindowTitle("Edit event")
            self.new_name_label.setText("Name")
            self.new_date_label.setText("Date")
            self.new_hour_label.setText("Hour")
            self.new_location_label.setText("Location")
            self.ok_button.setText("Ok")
            self.cancel_button.setText("Cancel")

        self.setLayout(layout)

    def get_new_data(self):
        data_dic = {'name': self.new_name.text(), 'date': self.new_date.text(), 'hour': self.new_hour.text(), 'location': self.new_location.text()}
        return data_dic
        