from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QWidget, QMenu, QInputDialog, QMessageBox

from src.menus.task.task_menu import TaskMenu
from src.main import MainWindow

from src.menus.task.task_display import TaskOngoingDisplay, TaskFinishedDisplay
from src.menus.task.task_list_menu import TaskMenu
from src.menus.task.favorite_task_menu import FavoriteTaskMenu

class TaskPage(QWidget) :
    def __init__(self, mainpage: MainWindow):
        '''
        Initialise la page d'acceuil du logiciel
        '''
        super().__init__(mainpage)
        self.ui = mainpage.ui
        self.mainpage = mainpage

        # initialisation de l'affichage
        self.show_ongoing_task()
        self.ui.pages_tasks.setCurrentIndex(0)

        # changement de page vers evenement
        self.ui.event_button_2.clicked.connect(self.goto_event)

        # ajout tache
        self.ui.new_task_button.clicked.connect(lambda: self.add_task(mainpage))

        #visualiser tâches terminées ou en cours
        self.ui.finished_task_button.clicked.connect(self.show_finished_task)
        self.ui.back_ftask_button.clicked.connect(self.show_ongoing_task)

        # gestion liste d'agenda
        self.ui.mytask_box.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.mytask_box.customContextMenuRequested.connect(self.show_task_menu)

        # gestion liste favoris
        self.ui.followedtask_box.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.followedtask_box.customContextMenuRequested.connect(self.show_task_favorite_menu)


############################# gestion changement task to event page ################################
    def goto_event(self):
        '''
        Change la page d'affichage du logiciel à la page d'evenement
        :return: None
        '''
        self.ui.pages_logiciel.setCurrentIndex(3)

############################# gestion ajout evenement ################################
    def add_task(self, mainpage: MainWindow):
        '''
        Permet la création d'un nouvel événement et ouverture du menu de parametrage
        :return: None
        '''
        param_task = TaskMenu(mainpage, self)
        if param_task.exec():
            print(param_task.get_data())

############################# gestion affichage taches finies ################################
    def show_finished_task(self):
        curr_task_list = self.ui.mytask_box.currentText() # récupération de la liste d'event actuellement selectionée par l'utilisateur
        task_list = TaskFinishedDisplay(self.ui.frame_7, curr_task_list)
        self.ui.pages_tasks.setCurrentIndex(1)

############################# gestion affichage taches finies ################################
    def show_ongoing_task(self):
        curr_task_list = self.ui.mytask_box.currentText()  # récupération de la liste d'event actuellement selectionée par l'utilisateur
        task_list = TaskOngoingDisplay(self.ui.frame_task,curr_task_list)
        self.ui.pages_tasks.setCurrentIndex(0)


############################# gestion liste taches #########################################

    def show_task_menu(self, pos: QPoint):
        '''
        Permet d'ajouter ou supprimer une liste de tâche dans la liste des tâches de l'utilisateur
        #TODO Léo: Mémoriser ces ajouts et supression quelque pars
        :param pos: Position du menu (en fonction du clic droit)
        :return: None
        '''
        menu = TaskMenu(self.ui.mytask_box,self.mainpage,pos,self)

    ############################# gestion liste favoris agenda #########################################

    def show_task_favorite_menu(self, pos: QPoint):
        '''
        Permet d'ajouter ou supprimer une liste de tâche dans la liste des favoris de l'utilisateur
        #TODO Léo: Mémoriser ces ajouts et supression quelque pars
        :param pos: Position du menu (en fonction du clic droit)
        :return: None
        '''
        menu = FavoriteTaskMenu(self.ui.followedtask_box,self.mainpage,pos,self)