from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QWidget, QMenu, QInputDialog, QMessageBox, QVBoxLayout

from src.menus.task.task_menu import TaskMenu
from src.main import MainWindow

from src.menus.task.task_display import TaskOngoingDisplay, TaskFinishedDisplay

import src.DAO as DAO

class TaskPage(QWidget) :
    def __init__(self, mainpage: MainWindow):
        '''
        Initialise la page d'acceuil du logiciel
        '''
        super().__init__(mainpage)
        self.ui = mainpage.ui
        self.mainpage = mainpage


        # initialisation de l'affichage
        self.ui.ongoing_task_display = TaskOngoingDisplay(self.mainpage, self.ui.frame_task)
        self.ui.finished_task_display = TaskFinishedDisplay(self.mainpage, self.ui.frame_7)
        self.show_ongoing_task()


        # changement de page vers evenement
        self.ui.event_button_2.clicked.connect(self.goto_event)

        # deconnexion
        self.ui.deconnect_button_t.clicked.connect(self.goto_login)

        # ajout tache
        self.ui.new_task_button.clicked.connect(lambda: self.add_task(mainpage))

        #visualiser tâches terminées ou en cours
        self.ui.finished_task_button.clicked.connect(self.show_finished_task)
        self.ui.back_ftask_button.clicked.connect(self.show_ongoing_task)


############################# gestion changement task to event page ################################
    def goto_event(self):
        '''
        Change la page d'affichage du logiciel à la page d'evenement
        :return: None
        '''
        self.ui.pages_logiciel.setCurrentIndex(3)

############################# gestion changement task to event page ################################
    def goto_login(self):
        '''
        Change la page d'affichage du logiciel à la page d'acceuil
        :return: None
        '''
        self.ui.pages_logiciel.setCurrentIndex(0)
        self.ui.myagenda_box.clear()
        self.ui.followedagenda_box.clear()

        text = self.ui.email_label_e.text()
        self.ui.email_label_e.setText(text[:len(text) - len(DAO.user.mail)])

        text = self.ui.email_label_t.text()
        self.ui.email_label_t.setText(text[:len(text) - len(DAO.user.mail)])

############################# gestion ajout evenement ################################
    def add_task(self, mainpage: MainWindow):
        '''
        Permet la création d'un nouvel événement et ouverture du menu de parametrage
        :return: None
        '''
        param_task = TaskMenu(mainpage, self)
        if param_task.exec():
            task = param_task.get_data()
            DAO.taskdao.insert(
                user=DAO.user,
                task=task
            )
            DAO.tasklist.append(task)
        self.ui.ongoing_task_display.refresh()

############################# gestion affichage taches finies ################################
    def show_finished_task(self):
        self.ui.pages_tasks.setCurrentIndex(1)


############################# gestion affichage taches finies ################################
    def show_ongoing_task(self):
        self.ui.pages_tasks.setCurrentIndex(0)
        self.ui.ongoing_task_display.refresh()
