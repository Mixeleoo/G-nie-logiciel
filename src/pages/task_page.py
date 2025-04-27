from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QWidget, QMenu, QInputDialog, QMessageBox

from menus.task.task_menu import TaskMenu
from main import MainWindow

class TaskPage(QWidget) :
    def __init__(self, mainpage: MainWindow):
        '''
        Initialise la page d'acceuil du logiciel
        '''
        super().__init__(mainpage)
        self.ui = mainpage.ui

        self.ui.event_button_2.clicked.connect(self.goto_event)

        # ajout tache
        self.ui.new_task_button.clicked.connect(lambda: self.add_task(mainpage))

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



############################# gestion liste taches #########################################

    def show_task_menu(self, pos: QPoint):
        '''
        Permet d'ajouter ou supprimer une liste de tâche dans la liste des tâches de l'utilisateur
        #TODO Léo: Mémoriser ces ajouts et supression quelque pars
        :param pos: Position du menu (en fonction du clic droit)
        :return: None
        '''
        menu = QMenu(self.ui.mytask_box)

        # gestion affichage du menu si la langue est le francais
        if self.ui.current_lang == "fr" :

            add_action = menu.addAction("Ajouter une liste de tâches")
            remove_action = None
            favorite_action = None

            # On n'ajoute l'option de supression ou d'ajout aux favoris que s'il y a un élément sélectionné
            current_index = self.ui.mytask_box.currentIndex()
            if current_index != -1:
                remove_action = menu.addAction("Supprimer la liste de tâches sélectionnée")
                favorite_action = menu.addAction("Ajouter la liste de tâches sélectionnée aux favoris")

            action = menu.exec(self.ui.mytask_box.mapToGlobal(pos))

            if action == add_action:
                text, ok = QInputDialog.getText(self, "Ajouter une liste de tâches", "Nom de la liste :")
                if ok and text:
                    self.ui.mytask_box.addItem(text)

            elif action == favorite_action:
                item_text = self.ui.mytask_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle(f"Confirmer l'ajout aux favoris")
                msg.setText(f"Voulez-vous ajouter « {item_text} » aux favoris?")

                btn_oui = msg.addButton("Oui", QMessageBox.ButtonRole.YesRole)
                btn_non = msg.addButton("Non", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_oui:
                    self.ui.followedtask_box.addItem(item_text)

            elif action == remove_action:
                item_text = self.ui.mytask_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle("Confirmer la suppression")
                msg.setText(f"Voulez-vous supprimer « {item_text} » ?")

                btn_oui = msg.addButton("Oui", QMessageBox.ButtonRole.YesRole)
                btn_non = msg.addButton("Non", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_oui:
                    self.ui.mytask_box.removeItem(current_index)

        # gestion et affichage du menu si la langue est l'anglais
        elif self.ui.current_lang == "en" :
            add_action = menu.addAction("Add a task list")
            remove_action = None
            favorite_action = None

            # On n'ajoute l'option de supression ou d'ajout aux favoris que s'il y a un élément sélectionné
            current_index = self.ui.mytask_box.currentIndex()
            if current_index != -1:
                remove_action = menu.addAction("Delete selected task list")
                favorite_action = menu.addAction("Add selected task list to favorite")

            action = menu.exec(self.ui.mytask_box.mapToGlobal(pos))

            # gestion de l'action d'ajout
            if action == add_action:
                text, ok = QInputDialog.getText(self, "Add a task list", "Task list name :")
                if ok and text:
                    self.ui.mytask_box.addItem(text)

            # gestion de l'action d'ajout aux favoris
            elif action == favorite_action:
                item_text = self.ui.mytask_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle(f"Add to favorite confirmation")
                msg.setText(f"Do you want to add « {item_text} » to favorite?")

                btn_yes = msg.addButton("Yes", QMessageBox.ButtonRole.YesRole)
                btn_no = msg.addButton("No", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_yes:
                    self.ui.followedtask_box.addItem(item_text)

            # gestion de l'action de supression
            elif action == remove_action:
                item_text = self.ui.mytask_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle("Delete confirmation")
                msg.setText(f"Do you want to delete « {item_text} » ?")

                btn_yes = msg.addButton("Yes", QMessageBox.ButtonRole.YesRole)
                btn_no = msg.addButton("No", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_yes:
                    self.ui.mytask_box.removeItem(current_index)

    ############################# gestion liste favoris agenda #########################################

    def show_task_favorite_menu(self, pos: QPoint):
        '''
        Permet d'ajouter ou supprimer une liste de tâche dans la liste des favoris de l'utilisateur
        #TODO Léo: Mémoriser ces ajouts et supression quelque pars
        :param pos: Position du menu (en fonction du clic droit)
        :return: None
        '''
        menu = QMenu(self.ui.followedtask_box)

        # gestion et affichage du menu si la langue est le francais
        if self.ui.current_lang == "fr":

            remove_action = None
            remove_favorite_action = None

            # On n'ajoute l'option de supression ou d'ajout aux favoris que s'il y a un élément sélectionné
            current_index = self.ui.followedtask_box.currentIndex()
            if current_index != -1:
                remove_action = menu.addAction("Supprimer la liste de tâche sélectionnée")
                remove_favorite_action = menu.addAction("Supprimer liste de tâche sélectionnée des favoris")

            action = menu.exec(self.ui.followedtask_box.mapToGlobal(pos))

            # supression d'un élément des favoris
            if action == remove_favorite_action :
                item_text = self.ui.followedtask_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle(f"Confirmer la suppression des favoris")
                msg.setText(f"Voulez-vous retirer « {item_text} » des favoris?")

                btn_oui = msg.addButton("Oui", QMessageBox.ButtonRole.YesRole)
                btn_non = msg.addButton("Non", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_oui:
                    self.ui.followedtask_box.removeItem(current_index)

            # supression d'un agenda via la liste des favoris
            elif action == remove_action:
                item_text = self.ui.followedtask_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle("Confirmer la suppression")
                msg.setText(f"Voulez-vous supprimer la liste de tâche « {item_text} » ?")

                btn_oui = msg.addButton("Oui", QMessageBox.ButtonRole.YesRole)
                btn_non = msg.addButton("Non", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_oui:
                    self.ui.mytask_box.removeItem(self.ui.mytask_box.findText(item_text)) #suppression des liste de taches en récupérant son indice à l'aide de son nom
                    self.ui.followedtask_box.removeItem(current_index) # suppression des favoris

        # gestion et affichage du menu si la langue est l'anglais
        elif self.ui.current_lang == "en":
            remove_action = None
            remove_favorite_action = None

            # On n'ajoute l'option de supression ou d'ajout aux favoris que s'il y a un élément sélectionné
            current_index = self.ui.followedtask_box.currentIndex()
            if current_index != -1:
                remove_action = menu.addAction("Delete selected task list")
                remove_favorite_action = menu.addAction("Remove selected task list from favorite")

            action = menu.exec(self.ui.followedtask_box.mapToGlobal(pos))

            # gestion de l'action de suppression des favoris
            if action == remove_favorite_action:
                item_text = self.ui.followedtask_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle(f"Remove from favorite confirmation")
                msg.setText(f"Do you want to remove « {item_text} » from favorite?")

                btn_yes = msg.addButton("Yes", QMessageBox.ButtonRole.YesRole)
                btn_no = msg.addButton("No", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_yes:
                    self.ui.followedtask_box.removeItem(current_index)

            # gestion de l'action de supression de l'agenda via favoris
            elif action == remove_action:
                item_text = self.ui.mytask_box.currentText()

                msg = QMessageBox(self)
                msg.setWindowTitle("Delete confirmation")
                msg.setText(f"Do you want to delete task list « {item_text} » ?")

                btn_yes = msg.addButton("Yes", QMessageBox.ButtonRole.YesRole)
                btn_no = msg.addButton("No", QMessageBox.ButtonRole.NoRole)

                msg.exec()

                if msg.clickedButton() == btn_yes:
                    self.ui.mytask_box.removeItem(self.ui.mytask_box.findText(item_text))  # suppression des agenda en récupérant son indice à l'aide de son nom
                    self.ui.followedtask_box.removeItem(current_index)  # suppression des favoris