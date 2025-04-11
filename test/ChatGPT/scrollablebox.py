from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QRadioButton, QScrollArea, QPushButton
from PyQt5.QtCore import Qt

class Fenetre(QWidget):
    def __init__(self):
        super().__init__()

        # Créer le layout principal
        self.layout = QVBoxLayout(self)

        # Créer une QGroupBox pour contenir les boutons radio
        self.group_box = QGroupBox("Choisissez une option", self)
        self.group_box.setFixedHeight(200)  # Fixer la hauteur de la QGroupBox
        self.group_box.setFixedWidth(200)  # Fixer la largeur de la QGroupBox

        # Créer un layout pour la QGroupBox
        self.radio_layout = QVBoxLayout(self.group_box)

        # Ajouter quelques boutons radio au départ
        self.radio1 = QRadioButton("Option 1")
        self.radio2 = QRadioButton("Option 2")
        self.radio3 = QRadioButton("Option 3")

        self.radio_layout.addWidget(self.radio1)
        self.radio_layout.addWidget(self.radio2)
        self.radio_layout.addWidget(self.radio3)

        # Créer une QScrollArea et y ajouter la QGroupBox
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.group_box)  # La QGroupBox devient scrollable

        # Ajouter la QScrollArea au layout principal
        self.layout.addWidget(self.scroll_area)

        # Ajouter un bouton pour ajouter dynamiquement un bouton radio
        self.add_button = QPushButton("Ajouter un bouton radio", self)
        self.add_button.clicked.connect(self.ajouter_radio)
        self.layout.addWidget(self.add_button)

        self.setWindowTitle("QGroupBox Scrollable avec QRadioButtons")
        self.setLayout(self.layout)
        self.show()

    def ajouter_radio(self):
        # Ajouter un nouveau bouton radio à la QGroupBox sans changer sa taille
        nouvelle_option = QRadioButton(f"Option {self.radio_layout.count() + 1}")
        self.radio_layout.addWidget(nouvelle_option)

if __name__ == "__main__":
    app = QApplication([])
    fenetre = Fenetre()
    app.exec_()