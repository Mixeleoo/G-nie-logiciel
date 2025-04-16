from PyQt6.QtWidgets import QWidget
from src.main import MainWindow

class TaskPage(QWidget) :
    def __init__(self, mainpage: MainWindow):
        '''
        Initialise la page d'acceuil du logiciel
        '''
        super().__init__(mainpage)
        self.ui = mainpage.ui

        self.ui.event_button_2.clicked.connect(self.goto_event)


############################# gestion changement task to event page ################################
    def goto_event(self):
        '''
        Change la page d'affichage du logiciel à la page d'evenement
        :return: None
        '''
        self.ui.pages_logiciel.setCurrentIndex(3)