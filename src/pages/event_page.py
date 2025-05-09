from PyQt6.QtCore import QDate, Qt, QPoint
from PyQt6.QtWidgets import QWidget
from src.main import MainWindow
from src.menus.event.event_menu import EventMenu
from src.menus.event.event_list_menu import EventListMenu
from src.menus.diaries.diary_menu import DiaryMenu
from src.menus.diaries.shared_diary_menu import SharedDiaryMenu
from menus.diaries.shared_agenda_page import SharedAgendaMenu

import src.DAO as DAO
from src.dataclass.event import Event

class EventPage(QWidget) :
    def __init__(self, mainpage: MainWindow):
        '''
        Initialise la page d'acceuil du logiciel
        '''
        super().__init__(mainpage)
        self.mainpage = mainpage
        self.ui = mainpage.ui

        self.current_date = QDate.currentDate() # date d'affichage par défaut

        # Dictionnaire qui servira à l'affichage du mois courant en fonction du language choisi
        self.months = { 'fr' : {1 : 'Janvier', 2 : 'Février', 3 : 'Mars', 4 : 'Avril', 5 : 'Mai', 6 : 'Juin', 7 : 'Juillet', 8 : 'Août', 9 : 'Septembre', 10 : 'Octobre', 11 : 'Novembre', 12 : 'Décembre' } ,
                        'eng' : {1 : 'January', 2 : 'February', 3 : 'March',  4 : 'April', 5 : 'May', 6 : 'June', 7 : 'July', 8 : 'August', 9 : 'September', 10 : 'October', 11 : 'November', 12 : 'Décember'}}

        self.ui.task_button.clicked.connect(self.goto_task)

        self.ui.deconnect_button_e.clicked.connect(self.goto_login)

        # ajout evenement
        self.ui.New_event_button.clicked.connect(lambda : self.add_event(mainpage))

        # recuperation date cliquée affichage mois
        self.ui.calendarWidget_2.clicked.connect(self.get_date_month)

        # recuperation date cliquée affichage semaines
        self.ui.table_week.cellClicked.connect(self.get_date_week)

        # recuperation date cliquée affichage jours
        self.ui.table_days.cellClicked.connect(self.get_date_days)

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

        # gestion liste d'agenda
        self.ui.myagenda_box.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.myagenda_box.customContextMenuRequested.connect(self.show_diaries_menu)

        # gestion liste favoris
        self.ui.followedagenda_box.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.followedagenda_box.customContextMenuRequested.connect(self.show_diaries_shared_menu)

        self.ui.shared_agenda_button.clicked.connect(lambda : self.see_shared_agenda(mainpage))

############################# gestion changement event to task page ################################

    def goto_task(self):
        '''
        Change la page d'affichage du logiciel à la page des taches
        :return: None
        '''
        self.ui.pages_logiciel.setCurrentIndex(4)

############################# gestion changement task to event page ################################
    def goto_login(self):
        '''
        Change la page d'affichage du logiciel à la page d'acceuil
        :return: None
        '''
        self.ui.pages_logiciel.setCurrentIndex(0)
        self.ui.mytask_box.clear()
        self.ui.myagenda_box.clear()
        self.ui.followedtask_box.clear()
        self.ui.followedagenda_box.clear()

        # on réintialise l'email écrit dans les carrés "info"
        text = self.ui.email_label_e.text()
        self.ui.email_label_e.setText(text[:len(text)-len(DAO.user.mail)])

        text = self.ui.email_label_t.text()
        self.ui.email_label_t.setText(text[:len(text) - len(DAO.user.mail)])

############################# gestion ajout evenement ################################
    def add_event(self, mainpage: MainWindow):
        '''
        Permet la création d'un nouvel événement et ouverture du menu de parametrage
        :return: None
        '''
        param_event = EventMenu(mainpage,self)
        if param_event.exec():
            event: Event = param_event.get_data()

            DAO.eventdao.insert(
                agenda=DAO.agendalist[event.id], # Oui j'utilise l'id pour l'index de l'agenda selectionné Y'A QUOI
                event=event
            )

############################# gestion ajout evenement ################################
    def see_event(self, mainpage : MainWindow, date : QDate):
        '''
        Affichage des evenements de la date courante
        :param mainpage: Page event
        :param date: date cliquée
        :return: None
        '''
        try :
            display_event = EventListMenu(mainpage,self, date)
            display_event.exec()
        except Exception as e :
            raise e

############################# gestion agenda partagés ################################
    def see_shared_agenda(self, mainpage: MainWindow):
        '''
        Affichage des evenements de la date courante
        :param mainpage: Page event
        :return: None
        '''
        try :
            display_shared_agenda = SharedAgendaMenu(mainpage, self)
            if display_shared_agenda.exec():
                print('truc')
        except Exception as e :
            raise e

############################# gestion recuperation date cliquée ################################
    def get_date_month(self, date : QDate):
        try :
            self.see_event(self.mainpage,date)
        except Exception as e:
            raise e

############################# gestion recuperation date cliquée ################################
    def get_date_week(self, row, column) :
        '''
        Permet de récupérer la date du jour indiquée dans la colonne cliquée du tableau pour trouver les evenement associés

       :param row: Indice de la ligne cliquée du tableau
       :param column: Indice de la colonne cliquée du tableau
       :return: Date de la colonne courante
       '''
        title = self.ui.table_week.horizontalHeaderItem(column).text() # recuperation de la date de la colonne cliquée
        print(title[4:])

############################# gestion recuperation date cliquée ################################
    def get_date_days(self, row, column):
        '''
        Permet de récupérer la date du jour indiquée dans la colonne du tableau pour trouver les evenement associés

        :param row: Indice de la ligne cliquée du tableau
        :param column: Indice de la colonne cliquée du tableau
        :return: Date de la colonne courante
        '''
        title = self.ui.table_days.horizontalHeaderItem(column).text()  # recuperation de la date de la colonne cliquée
        date = title[4:] # date courante
        print(title[4:])

        return date

############################# gestion choix affichage #########################################
    def set_months_display(self, checked):
        '''
        Passe l'affichage du calendrier par mois
        :return: None
        '''
        try:
            self.ui.pages_calendrier.setCurrentIndex(0)
            self.ui.curr_display_date.setText(self.current_date.toString('yyyy'))
        except Exception as e:
            print(f"Erreur dans set_months_display: {e}")

    def set_weeks_display(self, checked):
        '''
        Passe l'affichage du calendrier par semaines
        :return: None
        '''
        try:
            self.ui.pages_calendrier.setCurrentIndex(1)
            self.ui.curr_display_date.setText(self.months[self.ui.current_lang][int(self.current_date.toString('MM'))])
        except Exception as e:
            print(f"Erreur dans set_weeks_display: {e}")


    def set_days_display(self, checked):
        '''
        Passe l'affichage du calendrier par jour
        :return: None
        '''
        try:
            self.ui.pages_calendrier.setCurrentIndex(2)
            self.ui.curr_display_date.setText(self.months[self.ui.current_lang][int(self.current_date.toString('MM'))])
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
            self.ui.curr_display_date.setText(self.months[self.ui.current_lang][int(self.current_date.toString('MM'))])
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
            self.ui.curr_display_date.setText(self.months[self.ui.current_lang][int(self.current_date.toString('MM'))])
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
            self.ui.curr_display_date.setText(self.months[self.ui.current_lang][int(self.current_date.toString('MM'))])
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
            self.ui.curr_display_date.setText(self.months[self.ui.current_lang][int(self.current_date.toString('MM'))])
        except Exception as e:
            print(f"Erreur dans next_day: {e}")

    def add_agenda(self):
        '''
        Ajouter un agenda à la liste d'agenda
        :return: None
        '''

############################# gestion liste agenda #########################################

    def show_diaries_menu(self, pos: QPoint):
        '''
        Permet d'ajouter ou supprimer un agenda dans la liste d'agenda de l'utilisateur
        :param pos: Position du menu (en fonction du clic droit)
        :return: None
        '''
        menu = DiaryMenu(self.ui.myagenda_box, self.mainpage,pos,self)

    ############################# gestion liste favoris agenda #########################################

    def show_diaries_shared_menu(self, pos: QPoint):
        '''
        Permet d'ajouter ou supprimer un agenda dans la liste des favoris de l'utilisateur
        :param pos: Position du menu (en fonction du clic droit)
        :return: None
        '''
        menu = SharedDiaryMenu(self.ui.followedagenda_box,self.mainpage,pos,self)