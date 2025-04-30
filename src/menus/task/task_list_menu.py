from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QMenu, QInputDialog, QMessageBox

translate_dic = {
    'fr': ["Ajouter une tâche", "Supprimer la tâche sélectionné", "Ajouter la tâche sélectionné aux favoris",
           "Modifier la tâche sélectionné", "Ajouter une tâche", "Nom de la tâche :", "Confirmer l'ajout aux favoris",
           "Voulez-vous ajouter", "aux favoris?", "Oui", "Non", "Confirmer la suppression", "Voulez-vous supprimer"],
    'en': ["Add a task", "Delete selected task", "Add selected task to favorite", "Edit selected task",
           "Add a task", "task name :", "Add to favorite confirmation", "Do you want to add", "to favorite?", "Yes",
           "No", "Delete confirmation", "Do you want to delete"]}


class TaskListMenu(QMenu):
    @property
    def phrase(self) -> list[str]:
        return translate_dic[self.ui.current_lang]

    def __init__(self, taskbox, mainpage, pos: QPoint, taskpage):
        super().__init__(parent=taskbox)
        self.ui = mainpage.ui

        self.share_input = None

        self.add_action = self.addAction(self.phrase[0])
        self.edit_action = None
        self.remove_action = None
        self.favorite_action = None

        current_index = self.ui.mytask_box.currentIndex()
        if current_index != -1:
            self.favorite_action = self.addAction(self.phrase[2])
            self.remove_action = self.addAction(self.phrase[1])
            self.edit_action = self.addAction(self.phrase[3])

        action = self.exec(self.ui.mytask_box.mapToGlobal(pos))

        if action == self.add_action:
            text, ok = QInputDialog.getText(self, self.phrase[4], self.phrase[5])
            if ok and text:
                #TODO Léo: Mémoriser ces ajouts quelque pars
                self.ui.mytask_box.addItem(text)

        elif action == self.edit_action:
            try :
                text, ok = QInputDialog.getText(self, self.phrase[3], self.phrase[5])
                if ok and text:
                    # TODO gérer modification d'une liste de tache dans la bd
                    self.ui.mytask_box.setItemText(self.ui.mytask_box.currentIndex(), text)
            except Exception as e:
                print(e)

        elif action == self.favorite_action:
            item_text = self.ui.mytask_box.currentText()

            msg = QMessageBox(taskpage)
            msg.setWindowTitle(self.phrase[6])
            msg.setText(f"{self.phrase[7]} « {item_text} » {self.phrase[8]}")

            btn_oui = msg.addButton(self.phrase[9], QMessageBox.ButtonRole.YesRole)
            btn_non = msg.addButton(self.phrase[10], QMessageBox.ButtonRole.NoRole)

            msg.exec()

            if msg.clickedButton() == btn_oui:
                self.ui.followedtask_box.addItem(item_text)

        elif action == self.remove_action:
            # TODO Léo: Mémoriser ces supression quelque pars

            item_text = self.ui.mytask_box.currentText()

            msg = QMessageBox(taskpage)
            msg.setWindowTitle(self.phrase[11])
            msg.setText(f"{self.phrase[12]} « {item_text} » ?")

            btn_oui = msg.addButton(self.phrase[9], QMessageBox.ButtonRole.YesRole)
            btn_non = msg.addButton(self.phrase[10], QMessageBox.ButtonRole.NoRole)

            msg.exec()

            if msg.clickedButton() == btn_oui:
                self.ui.followedtask_box.removeItem(self.ui.followedtask_box.findText(item_text))  # suppression des tâches en récupérant son indice à l'aide de son nom
                self.ui.mytask_box.removeItem(current_index)  # suppression de la tâche sélectionné

