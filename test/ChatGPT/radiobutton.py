from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QGroupBox, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class Fenetre(QWidget):
    def __init__(self):
        super().__init__()

        # Créer un layout vertical
        self.layout = QVBoxLayout(self)

        # Créer un QGroupBox pour regrouper les boutons radio
        self.group_box = QGroupBox("Choisissez une option", self)
        self.layout.addWidget(self.group_box)

        # Créer un layout horizontal pour les boutons radio
        self.radio_layout = QVBoxLayout()

        # Créer plusieurs boutons radio
        self.radio1 = QRadioButton("Option 1")
        self.radio2 = QRadioButton("Option 2")
        self.radio3 = QRadioButton("Option 3")

        # Ajouter les boutons radio au layout
        self.radio_layout.addWidget(self.radio1)
        self.radio_layout.addWidget(self.radio2)
        self.radio_layout.addWidget(self.radio3)

        # Ajouter le layout des boutons radio au group box
        self.group_box.setLayout(self.radio_layout)

        # Créer un bouton pour récupérer la sélection
        self.button = QPushButton("Afficher la sélection", self)
        self.layout.addWidget(self.button)

        # Connecter le bouton à une fonction qui récupère la sélection
        self.button.clicked.connect(self.afficher_selection)

        # Initialiser le widget
        self.setLayout(self.layout)
        self.setWindowTitle("Exemple Liste de Boutons Radio")
        self.show()

    def afficher_selection(self):
        # Vérifier quel bouton radio est sélectionné
        if self.radio1.isChecked():
            print("Option 1 sélectionnée")
        elif self.radio2.isChecked():
            print("Option 2 sélectionnée")
        elif self.radio3.isChecked():
            print("Option 3 sélectionnée")
        else:
            print("Aucune option sélectionnée")

if __name__ == '__main__':
    app = QApplication([])
    fenetre = Fenetre()
    app.exec_()