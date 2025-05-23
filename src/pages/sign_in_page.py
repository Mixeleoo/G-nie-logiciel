from PyQt6.QtWidgets import QWidget
from src.main import MainWindow
import src.DAO as DAO
from src.dataclass.user import User

class SignInPage(QWidget) :
    def __init__(self, mainpage: MainWindow):
        '''
        Initialise la page de création de compte du logiciel
        : param mainpage: Fenêtre du logiciel
        '''
        super().__init__(mainpage)
        self.ui = mainpage.ui

        self.ui.back_button_2.clicked.connect(lambda : self.goto_homepage())
        self.ui.validate_account_button.clicked.connect(lambda : self.validate_acccount())

        # suppression messages d'erreur
        self.ui.error_label2.hide()
        self.ui.error_label3.hide()
        self.ui.error_label4.hide()
        self.ui.email_line_connection_2.textEdited.connect(lambda: self.clear_error())
        self.ui.password_line_connection_2.textEdited.connect(lambda: self.clear_error())
        self.ui.passwordconfirm_line_connection_2.textEdited.connect(lambda: self.clear_error())

    def goto_homepage(self):
        '''
        Change la page du logiciel à la page d'acceuil
        :return: None
        '''
        self.ui.pages_logiciel.setCurrentIndex(0) # homepage
        # suppression des messages d'erreur et contenu input
        self.clear_all()

    def validate_acccount(self):
        '''
        'Vérifie que les données entrées par l'utilisateur sont correctes et ajoute le compte dans la base de données
        :return: None
        '''

        user = User(mail=self.ui.email_line_connection_2.text(), mdp=self.ui.password_line_connection_2.text())

        if not self.check_password_repeat():
            self.ui.error_label2.show()

        elif self.ui.email_line_connection_2.text().strip() == "" or DAO.userdao.is_valid(user):
            self.ui.error_label3.show()
        elif self.ui.password_line_connection_2.text().strip() == "" or self.ui.passwordconfirm_line_connection_2.text().strip() == "":
            self.ui.error_label4.show()
        else :
            self.ui.pages_logiciel.setCurrentIndex(1) # ouvre la page de connexion
            DAO.userdao.insert(user)
            self.clear_all()

    def check_password_repeat(self) -> bool:
        '''
        Vérifie si le mot de passe répété et bien le même
        :return: True si oui et False sinon
        '''
        return self.ui.password_line_connection_2.text() == self.ui.passwordconfirm_line_connection_2.text()

    def clear_all(self):
        '''
        Vide tous les input et efface les messages d'erreur
        '''
        self.ui.password_line_connection_2.clear()
        self.ui.passwordconfirm_line_connection_2.clear()
        self.ui.email_line_connection_2.clear()
        self.clear_error()

    def clear_error(self):
        '''
        Supprime les messages d'erreur
        :return: None
        '''
        self.ui.error_label2.hide()
        self.ui.error_label3.hide()
        self.ui.error_label4.hide()