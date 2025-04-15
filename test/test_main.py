import sys
from PyQt6.QtWidgets import QApplication, QWidget
from src.ui.software_ui import Ui_sofware_ui


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_sofware_ui()
        self.ui.setupUi(self)


       # Connexion des boutons pour le changement de langue
        self.ui.french_button.clicked.connect(lambda: self.change_language("fr"))
        self.ui.english_button.clicked.connect(lambda: self.change_language("en"))

        # Langue par défaut
        self.current_lang = "fr"
        self.change_language(self.current_lang)

    def change_language(self, lang):
        #print(f"\u2192 Langue sélectionnée : {lang}")
        if lang == "fr":
            self.ui.retranslateUi_french(self)
        elif lang == "en":
            self.ui.retranslateUi_english(self)
        self.current_lang = lang


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())