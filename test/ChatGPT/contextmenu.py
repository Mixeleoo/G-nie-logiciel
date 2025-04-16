from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QComboBox, QVBoxLayout,
    QWidget, QMenu, QInputDialog
)
from PyQt6.QtCore import Qt, QPoint

class CustomComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos: QPoint):
        menu = QMenu(self)
        add_action = menu.addAction("Ajouter")

        action = menu.exec(self.mapToGlobal(pos))
        if action == add_action:
            text, ok = QInputDialog.getText(self, "Ajouter un élément", "Nom de l'élément :")
            if ok and text:
                self.addItem(text)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ComboBox avec clic droit")
        self.combo = CustomComboBox()
        self.combo.addItems(["Élément 1", "Élément 2"])

        layout = QVBoxLayout()
        layout.addWidget(self.combo)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()