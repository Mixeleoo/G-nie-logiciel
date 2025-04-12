from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menu contextuel avec clic droit")
        self.setGeometry(100, 100, 400, 300)

        self.list_widget = QListWidget()
        self.setCentralWidget(self.list_widget)

        # Ajouter quelques éléments à la liste
        for i in range(5):
            self.list_widget.addItem(f"Élément {i + 1}")

        # Connecter le menu contextuel
        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        # Obtenir l'élément cliqué
        item = self.list_widget.itemAt(position)
        if item:
            menu = QMenu()

            modifier_action = menu.addAction("Modifier")
            renommer_action = menu.addAction("Renommer")
            supprimer_action = menu.addAction("Supprimer")

            action = menu.exec(self.list_widget.mapToGlobal(position))

            if action == modifier_action:
                QMessageBox.information(self, "Action", f"Modifier: {item.text()}")
            elif action == renommer_action:
                QMessageBox.information(self, "Action", f"Renommer: {item.text()}")
            elif action == supprimer_action:
                QMessageBox.information(self, "Action", f"Supprimer: {item.text()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())