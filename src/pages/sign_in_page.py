from PyQt6.QtWidgets import QWidget
from src.main import MainWindow

class SignInPage(QWidget) :
    def __init__(self, mainpage: MainWindow):
        '''
        Initialise la page d'acceuil du logiciel
        '''
        super().__init__(mainpage)
        self.ui = mainpage.ui

        self.ui.back_button_2.clicked.connect(lambda : self.goto_homepage())

    def goto_homepage(self):
        '''
        Change la page du logiciel à la page d'acceuil
        :return: None
        '''
        self.ui.pages_logiciel.setCurrentIndex(0) # homepage