from PyQt6.QtCore import QDate, Qt, QPoint
from PyQt6.QtWidgets import QWidget, QMenu, QInputDialog, QMessageBox, QDialog, QLineEdit, QVBoxLayout, QLabel
from src.main import MainWindow
from src.menus.event_menu import EventMenu
from src.menus.event_list_menu import EventListMenu

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
        self.ui.followedagenda_box.customContextMenuRequested.connect(self.show_diaries_favorite_menu)

############################# gestion changement event to task page ################################

    def goto_task(self):
        '''
        Change la page d'affichage du logiciel à la page des taches
        :return: None
        '''
        self.ui.pages_logiciel.setCurrentIndex(4)

############################# gestion ajout evenement ################################
    def add_event(self, mainpage: MainWindow):
        '''
        Permet la création d'un nouvel événement et ouverture du menu de parametrage
        :return: None
        '''
        param_event = EventMenu(mainpage,self)
        if param_event.exec() :
            print(param_event.get_data())

############################# gestion ajout evenement ################################
    def see_event(self, mainpage : MainWindow, date : QDate):
        try :
            display_event = EventListMenu(mainpage,self, date)
            print(date)
            if display_event.exec() :
                print('truc')
        except Exception as e :
            print(f"Erreur dans see_event: {e}")

############################# gestion recuperation date cliquée ################################
    def get_date_month(self, date : QDate):
        print(f"{date.toString('dd/MM/yyyy')}")
        self.see_event(self.mainpage,date)

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
        #TODO Léo: Mémoriser ces ajouts et supression quelque pars
        :param pos: Position du menu (en fonction du clic droit)
        :return: None
        '''
        menu = QMenu(self.ui.myagenda_box)

        # gestion affichage du menu si la langue est le francais
        if self.ui.current_lang == "fr" :

            add_action = menu.addAction("Ajouter un agenda")
            remove_action = None
            favorite_action = None

            # On n'ajoute l'option de supression ou d'ajout aux favoris que s'il y a un élément sélectionné
            current_index = self.ui.myagenda_box.currentIndex()
            if current_index != -1:
                remove_action = menu.addAction("Supprimer l'agenda sélectionné")
                favorite_action = menu.addAction("Ajouter l'agenda sélectionné aux favoris")

            action = menu.exec(self.ui.myagenda_box.mapToGlobal(pos))

            if action == add_action:
                text, ok = QInputDialog.getText(self, "Ajouter un agenda", "Nom de l'agenda :")
                if ok and text:
                    self.ui.myagenda_box.addItem(text)

            elif action == favorite_action:
                item_text = self.ui.myagenda_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle(f"Confirmer l'ajout aux favoris")
                msg.setText(f"Voulez-vous ajouter « {item_text} » aux favoris?")

                btn_oui = msg.addButton("Oui", QMessageBox.ButtonRole.YesRole)
                btn_non = msg.addButton("Non", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_oui:
                    self.ui.followedagenda_box.addItem(item_text)

            elif action == remove_action:
                item_text = self.ui.myagenda_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle("Confirmer la suppression")
                msg.setText(f"Voulez-vous supprimer « {item_text} » ?")

                btn_oui = msg.addButton("Oui", QMessageBox.ButtonRole.YesRole)
                btn_non = msg.addButton("Non", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_oui:
                    self.ui.myagenda_box.removeItem(current_index)

        # gestion et affichage du menu si la langue est l'anglais
        elif self.ui.current_lang == "en" :
            add_action = menu.addAction("Add a diary")
            remove_action = None
            favorite_action = None

            # On n'ajoute l'option de supression ou d'ajout aux favoris que s'il y a un élément sélectionné
            current_index = self.ui.myagenda_box.currentIndex()
            if current_index != -1:
                remove_action = menu.addAction("Delete selected diary")
                favorite_action = menu.addAction("Add selected diary to favorite")

            action = menu.exec(self.ui.myagenda_box.mapToGlobal(pos))

            # gestion de l'action d'ajout
            if action == add_action:
                text, ok = QInputDialog.getText(self, "Add a diary", "Diary name :")
                if ok and text:
                    self.ui.myagenda_box.addItem(text)

            # gestion de l'action d'ajout aux favoris
            elif action == favorite_action:
                item_text = self.ui.myagenda_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle(f"Add to favorite confirmation")
                msg.setText(f"Do you want to add « {item_text} » to favorite?")

                btn_yes = msg.addButton("Yes", QMessageBox.ButtonRole.YesRole)
                btn_no = msg.addButton("No", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_yes:
                    self.ui.followedagenda_box.addItem(item_text)

            # gestion de l'action de supression
            elif action == remove_action:
                item_text = self.ui.myagenda_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle("Delete confirmation")
                msg.setText(f"Do you want to delete « {item_text} » ?")

                btn_yes = msg.addButton("Yes", QMessageBox.ButtonRole.YesRole)
                btn_no = msg.addButton("No", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_yes:
                    self.ui.myagenda_box.removeItem(current_index)

    ############################# gestion liste favoris agenda #########################################

    def show_diaries_favorite_menu(self, pos: QPoint):
        '''
        Permet d'ajouter ou supprimer un agenda dans la liste des favoris de l'utilisateur
        #TODO Léo: Mémoriser ces ajouts et supression quelque pars
        :param pos: Position du menu (en fonction du clic droit)
        :return: None
        '''
        menu = QMenu(self.ui.followedagenda_box)

        # gestion et affichage du menu si la langue est le francais
        if self.ui.current_lang == "fr":

            remove_action = None
            remove_favorite_action = None

            # On n'ajoute l'option de supression ou d'ajout aux favoris que s'il y a un élément sélectionné
            current_index = self.ui.followedagenda_box.currentIndex()
            if current_index != -1:
                remove_action = menu.addAction("Supprimer l'agenda sélectionné")
                remove_favorite_action = menu.addAction("Supprimer l'agenda sélectionné des favoris")

            action = menu.exec(self.ui.followedagenda_box.mapToGlobal(pos))

            # supression d'un élément des favoris
            if action == remove_favorite_action :
                item_text = self.ui.followedagenda_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle(f"Confirmer la suppression des favoris")
                msg.setText(f"Voulez-vous retirer « {item_text} » des favoris?")

                btn_oui = msg.addButton("Oui", QMessageBox.ButtonRole.YesRole)
                btn_non = msg.addButton("Non", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_oui:
                    self.ui.followedagenda_box.removeItem(current_index)

            # supression d'un agenda via la liste des favoris
            elif action == remove_action:
                item_text = self.ui.followedagenda_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle("Confirmer la suppression")
                msg.setText(f"Voulez-vous supprimer l'agenda « {item_text} » ?")

                btn_oui = msg.addButton("Oui", QMessageBox.ButtonRole.YesRole)
                btn_non = msg.addButton("Non", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_oui:
                    self.ui.myagenda_box.removeItem(self.ui.myagenda_box.findText(item_text)) #suppression des agenda en récupérant son indice à l'aide de son nom
                    self.ui.followedagenda_box.removeItem(current_index) # suppression des favoris

        # gestion et affichage du menu si la langue est l'anglais
        elif self.ui.current_lang == "en":
            remove_action = None
            remove_favorite_action = None

            # On n'ajoute l'option de supression ou d'ajout aux favoris que s'il y a un élément sélectionné
            current_index = self.ui.followedagenda_box.currentIndex()
            if current_index != -1:
                remove_action = menu.addAction("Delete selected diary")
                remove_favorite_action = menu.addAction("Remove selected diary from favorite")

            action = menu.exec(self.ui.followedagenda_box.mapToGlobal(pos))

            # gestion de l'action de suppression des favoris
            if action == remove_favorite_action:
                item_text = self.ui.followedagenda_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle(f"Remove from favorite confirmation")
                msg.setText(f"Do you want to remove « {item_text} » from favorite?")

                btn_yes = msg.addButton("Yes", QMessageBox.ButtonRole.YesRole)
                btn_no = msg.addButton("No", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_yes:
                    self.ui.followedagenda_box.removeItem(current_index)

            # gestion de l'action de supression de l'agenda via favoris
            elif action == remove_action:
                item_text = self.ui.myagenda_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle("Delete confirmation")
                msg.setText(f"Do you want to delete diary « {item_text} » ?")

                btn_yes = msg.addButton("Yes", QMessageBox.ButtonRole.YesRole)
                btn_no = msg.addButton("No", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_yes:
                    self.ui.myagenda_box.removeItem(self.ui.myagenda_box.findText(item_text))  # suppression des agenda en récupérant son indice à l'aide de son nom
                    self.ui.followedagenda_box.removeItem(current_index)  # suppression des favoris