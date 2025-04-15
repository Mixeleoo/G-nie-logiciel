from PyQt6.QtWidgets import QWidget
from src.main import MainWindow

class EventPage(QWidget) :
    def __init__(self, mainpage: MainWindow):
        '''
        Initialise la page d'acceuil du logiciel
        '''
        super().__init__(mainpage)
        self.ui = mainpage.ui

        # gestion choix d'affichage
        self.ui.radioYear.setChecked(True) # affichage par défaut Mois
        self.ui.radioYear.toggled.connect(lambda checked: self.set_months_display(checked))
        self.ui.radioWeek.toggled.connect(lambda checked: self.set_weeks_display(checked))
        self.ui.radioDay.toggled.connect(lambda checked : self.set_days_display(checked))

        # parcours de l'affichage par semaines


    def set_months_display(self, checked):
        '''
        Passe l'affichage du calendrier par mois
        :return: None
        '''
        try:
            self.ui.pages_calendrier.setCurrentIndex(0)
        except Exception as e:
            print(f"Erreur dans set_months_display: {e}")

    def set_weeks_display(self, checked):
        '''
        Passe l'affichage du calendrier par semaines
        :return: None
        '''
        try:
            self.ui.pages_calendrier.setCurrentIndex(1)
        except Exception as e:
            print(f"Erreur dans set_weeks_display: {e}")


    def set_days_display(self, checked):
        '''
        Passe l'affichage du calendrier par jour
        :return: None
        '''
        try:
            self.ui.pages_calendrier.setCurrentIndex(2)
        except Exception as e:
            print(f"Erreur dans set_days_display: {e}")