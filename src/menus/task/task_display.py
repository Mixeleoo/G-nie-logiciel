from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMenu, QListWidgetItem

import src.DAO as DAO
from src.dataclass.task import Task

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

        self.refresh() #remplissage de la page

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

            task_index = self.row(item)
            task = DAO.ogtasklist[task_index]

            # gestion actions sur les tâches en cours
            if action == terminee_action:
                task.done = True
                DAO.taskdao.update(task)
                DAO.ogtasklist.pop(task_index)
                DAO.ftasklist.append(task)
                self.takeItem(self.currentRow())

            elif action == renommer_action:
                self.rename_task(task)

            elif action == modifier_action:
                self.edit_task(item, task_index)

            elif action == supprimer_action:
                DAO.taskdao.delete(task)
                DAO.ogtasklist.pop(task_index)
                self.takeItem(self.currentRow())

                self.refresh()

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

            self.refresh()

    def edit_task(self, item: QListWidgetItem, task_index: int):
        from src.menus.task.edit_task_menu import EditTaskMenu
        try :
            edit_menu = EditTaskMenu(self.mainpage, self, item)

            if edit_menu.exec():
                DAO.ogtasklist[task_index] = edit_menu.get_data()
                DAO.taskdao.update(DAO.ogtasklist[task_index])
                self.refresh()
        except Exception as e:
            print(e)

    def refresh(self):
        self.clear()
        print(DAO.ogtasklist)
        for task in DAO.ogtasklist:
            item = QtWidgets.QListWidgetItem(task.name)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.addItem(item)




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

        self.refresh() #remplissage de la page

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_task_menu)

    def show_task_menu(self, pos):
        a_lang = {'fr': ['En cours'],
                  'en': ['Ongoing']}

        item = self.itemAt(pos)
        task_index = self.row(item)
        task: Task = DAO.ftasklist[task_index]
        if item:
            menu = QMenu()

            encours_action = menu.addAction(a_lang[self.ui.current_lang][0])

            action = menu.exec(self.mapToGlobal(pos))

            # gestion actions sur les tâches terminées
            if action == encours_action:
                task.done = False
                DAO.taskdao.update(task)
                DAO.ftasklist.pop(task_index)
                DAO.ogtasklist.append(task)

                self.takeItem(self.currentRow())
                self.refresh()

    def refresh(self):
        self.clear()
        print(DAO.ftasklist)
        for task in DAO.ftasklist:
            item = QtWidgets.QListWidgetItem(task.name)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.addItem(item)