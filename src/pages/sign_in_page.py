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
        # suppression des messages d'erreur
        self.ui.error_label2.hide()
        self.ui.error_label3.hide()
        self.ui.error_label4.hide()

    def validate_acccount(self):
        '''

        :return:
        '''
        if not self.check_password_repeat() :
            self.ui.error_label2.show()
        elif self.ui.email_line_connection_2.text().strip() == "" :
            self.ui.error_label3.show()
        elif self.ui.password_line_connection_2.text().strip() == "" or self.ui.passwordconfirm_line_connection_2.text().strip() == "":
            self.ui.error_label4.show()
        else :
            print("compte cree")

    def check_password_repeat(self) -> bool:
        '''
        Vérifie si le mot de passe répété et bien le même
        :return: True si oui et False sinon
        '''
        return self.ui.password_line_connection_2.text() == self.ui.passwordconfirm_line_connection_2.text()

    def clear_error(self):
        '''

        :return:
        '''
        self.ui.error_label2.hide()
        self.ui.error_label3.hide()
        self.ui.error_label4.hide()