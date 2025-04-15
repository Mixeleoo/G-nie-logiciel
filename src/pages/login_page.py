from PyQt6.QtWidgets import QWidget
from src.main import MainWindow

class LoginPage(QWidget) :
    def __init__(self, mainpage: MainWindow):
        '''
        Initialise la page d'acceuil du logiciel
        '''
        super().__init__(mainpage)
        self.ui = mainpage.ui

        self.ui.back_button.clicked.connect(lambda : self.goto_homepage())

    def goto_homepage(self):
        '''
        Change la page du logiciel à la page d'acceuil
        :return: None
        '''
        self.ui.pages_logiciel.setCurrentIndex(0) # homepage

    def validate_connection(self):
        '''
        Connecte l'utilisateur si son identifiant et mot de passe sont corrects
        :return: None
        '''

    def check_connection(self):
        '''
        Verifie que l'identifiant et mot de passe tapé par l'utilisateur sont correct
        :return: retourne True si corrects et False sinon
        '''