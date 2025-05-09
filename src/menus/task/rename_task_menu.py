from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QLabel, QPushButton, QDialog


class RenameTaskMenu(QDialog) :
    def __init__(self, mainpage, taskpage):
        super().__init__(parent=taskpage)
        self.ui = mainpage.ui

        layout = QVBoxLayout(self)

        self.new_name_label = QLabel()
        self.new_name = QLineEdit()

        self.ok_button = QPushButton()
        self.cancel_button = QPushButton()

        layout.addWidget(self.new_name_label)
        layout.addWidget(self.new_name)

        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)



        if self.ui.current_lang == 'fr':
            self.setWindowTitle('Renommer Tâche')
            self.new_name_label.setText("Nom")
            self.ok_button.setText("Valider")
            self.cancel_button.setText("Annuler")

        elif self.ui.current_lang == 'en':
            self.setWindowTitle("Rename task")
            self.new_name_label.setText("Name")
            self.ok_button.setText("Ok")
            self.cancel_button.setText("Cancel")

    def get_new_name(self) -> str:
        return self.new_name.text()