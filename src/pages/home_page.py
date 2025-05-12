from PyQt6.QtWidgets import QWidget
from src.main import MainWindow

class HomePage(QWidget) :
    def __init__(self, mainpage : MainWindow):
        '''
        Initialise la page d'acceuil du logiciel
        : param mainpage: Fenêtre du logiciel
        '''
        super().__init__(mainpage)
        self.ui = mainpage.ui
        #self.current_lang = "fr" #langue par défaut du logiciel

        # Bouton d'action de changement de langue
        self.ui.french_button.clicked.connect(lambda  : self.change_language("fr"))
        self.ui.english_button.clicked.connect(lambda  : self.change_language("en"))

        self.ui.connect_button.clicked.connect(lambda : self.goto_login())
        self.ui.create_account_button.clicked.connect(lambda : self.goto_signin())

    def change_language(self, lang):
        '''
        Permet de changer la langue du logiciel du français vers l'anglais ou inversemement
        :param lang: langue vers laquelle traduire
        :return: None
        '''
        if lang != self.ui.current_lang :
            self.ui.current_lang = lang
            if lang == "fr":
                self.ui.retranslateUi_french(self)
            elif lang == "en":
                self.ui.retranslateUi_english(self)

    def goto_login(self):
        '''
        Change la page du logiciel vers la pages de connexion
        :return: None
        '''
        self.ui.pages_logiciel.setCurrentIndex(1) #login_page

    def goto_signin(self):
        '''
        Change la page du logiciel vers la page de création de compte
        :return: None
        '''
        self.ui.pages_logiciel.setCurrentIndex(2) #sign_in_page