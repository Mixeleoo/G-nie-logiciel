from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QListWidget, QMenu

import src.DAO as DAO
from src.dataclass.task import Task
from src.menus.task.edit_task_menu import EditTaskMenu

class TaskOngoingDisplay(QtWidgets.QListWidget):
    def __init__(self,mainpage, taskpage):
        super(TaskOngoingDisplay, self).__init__(taskpage)

        self.ui = mainpage.ui
        self.mainpage = mainpage

        self.setGeometry(50,40,710,570)

        # parametrage du font de la qlist
        font = QFont()
        font.setPointSize(15)
        self.setFont(font)

        # J'imagine que c'est ça que je dois faire
        print("TAMER\n\n", DAO.tasklist)
        for task in DAO.tasklist:
            print(task)
            item = QtWidgets.QListWidgetItem(task.name)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.addItem(item)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_task_menu)

    def show_task_menu(self, pos):
        a_lang = {'fr': ['Terminée','Renommer','Modifier','Supprimer'],
                  'en': ['Finished','Rename','Edit','Delete']}

        item = self.itemAt(pos)
        if item:
            menu = QMenu()

            terminee_action = menu.addAction(a_lang[self.ui.current_lang][0])
            renommer_action = menu.addAction(a_lang[self.ui.current_lang][1])
            modifier_action = menu.addAction(a_lang[self.ui.current_lang][2])
            supprimer_action = menu.addAction(a_lang[self.ui.current_lang][3])

            action = menu.exec(self.mapToGlobal(pos))

            task = DAO.tasklist[pos]

            # gestion actions sur les tâches en cours
            if action == terminee_action:
                task.done = True
                DAO.taskdao.update(task)
                print('t')

            elif action == renommer_action:
                self.rename_task(task)

            elif action == modifier_action:
                self.edit_task()

            elif action == supprimer_action:
                DAO.taskdao.delete(task)
                print('s')

    def rename_task(self, task: Task):
        '''
        Crée et ouvre une fenêtre pour permettre à l'utilisateur de renommer l'évenement choisi
        :return:
        '''
        from src.menus.task.rename_task_menu import RenameTaskMenu
        rename_page = RenameTaskMenu(self.mainpage, self)
        if rename_page.exec() :
            task.name = rename_page.get_new_name()
            DAO.taskdao.update(task)
            print(rename_page.get_new_name())

    def edit_task(self):
        edit_menu = EditTaskMenu(self.mainpage, self)
        if edit_menu.exec():
            print("merde")






class TaskFinishedDisplay(QtWidgets.QListWidget):
    def __init__(self, mainpage, taskpage):
        super(TaskFinishedDisplay, self).__init__(taskpage)

        self.setGeometry(50,40,710,570)

        self.ui = mainpage.ui

        # parametrage du font de la qlist
        font = QFont()
        font.setPointSize(15)
        font.setStrikeOut(True)
        self.setFont(font)

        for task in DAO.tasklist:
            if task.done:
                item = QtWidgets.QListWidgetItem(task.name)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.addItem(item)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_task_menu)

    def show_task_menu(self, pos):
        a_lang = {'fr': ['En cours'],
                  'en': ['Ongoing']}

        item = self.itemAt(pos)
        task: Task = DAO.tasklist[pos]
        if item:
            menu = QMenu()

            encours_action = menu.addAction(a_lang[self.ui.current_lang][0])

            action = menu.exec(self.mapToGlobal(pos))

            # gestion actions sur les tâches terminées
            if action == encours_action:
                task.done = True
                DAO.taskdao.update(task)

