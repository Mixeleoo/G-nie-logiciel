import sys
from PyQt6.QtWidgets import QApplication, QWidget
from ui.software_ui import Ui_sofware_ui

class MainWindow(QWidget) :
    def __init__(self):
        super().__init__()

        self.ui = Ui_sofware_ui()
        self.ui.setupUi(self)

        from pages.home_page import HomePage
        self.homepage = HomePage(self)

        from pages.login_page import LoginPage
        self.login = LoginPage(self)

        from pages.sign_in_page import SignInPage
        self.signin = SignInPage(self)

        from pages.event_page import EventPage
        self.event = EventPage(self)

        from pages.task_page import TaskPage
        self.task = TaskPage(self)

        #initialisation à la première page du logiciel : homepage
        self.ui.pages_logiciel.setCurrentIndex(0)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    sofware_ui = MainWindow()
    sofware_ui.show()
    sys.exit(app.exec())
