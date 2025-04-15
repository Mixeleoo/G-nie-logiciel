from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from src.main import MainWindow
import calendar

class EventPage(QWidget) :
    def __init__(self, mainpage: MainWindow):
        '''
        Initialise la page d'acceuil du logiciel
        '''
        super().__init__(mainpage)
        self.ui = mainpage.ui

        self.current_date = QDate.currentDate() # date d'affichage par défaut
        print(self.current_date.dayOfWeek())

        #self.set_week_headers(self.current_date)

        # gestion choix d'affichage
        self.ui.radioYear.setChecked(True) # affichage par défaut Mois
        self.ui.radioYear.toggled.connect(lambda checked: self.set_months_display(checked))
        self.ui.radioWeek.toggled.connect(lambda checked: self.set_weeks_display(checked))
        self.ui.radioDay.toggled.connect(lambda checked : self.set_days_display(checked))

        # parcours de l'affichage par semaines
        self.ui.next_week.clicked.connect(lambda : self.next_week())
        self.ui.prev_week.clicked.connect(lambda : self.prev_week())

        # parcours de l'affichage par jours
        self.ui.next_day.clicked.connect(lambda : self.next_day())
        self.ui.prev_day.clicked.connect(lambda : self.prev_day())


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

############################# gestion affichage semaine #########################################
    def prev_week(self):
        '''
        Change l'affichage à la semaine précédente
        :return: None
        '''
        try:
            self.current_date = self.current_date.addDays(-7)
            self.ui.set_week_headers(self.current_date,self.ui.current_lang)
        except Exception as e:
            print(f"Erreur dans prev_week: {e}")

    def next_week(self):
        '''
        Change l'affichage à la semaine suivante
        :return: None
        '''
        try:
            self.current_date = self.current_date.addDays(7)
            self.ui.set_week_headers(self.current_date,self.ui.current_lang)
        except Exception as e:
            print(f"Erreur dans next_week: {e}")

############################# gestion affichage jour #########################################

    def prev_day(self):
        '''
        Change l'affichage au jour suivant
        :return: None
        '''
        try:
            self.current_date = self.current_date.addDays(-1)
            self.ui.set_days_headers(self.current_date,self.ui.current_lang)
        except Exception as e:
            print(f"Erreur dans prev_day: {e}")

    def next_day(self):
        '''
        Change l'affichage au jour suivant
        :return: None
        '''
        try:
            self.current_date = self.current_date.addDays(1)
            self.ui.set_days_headers(self.current_date,self.ui.current_lang)
        except Exception as e:
            print(f"Erreur dans next_day: {e}")