from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QMenu, QMessageBox


class FavoriteTaskMenu(QMenu):
    def __init__(self, favoritebox, mainpage, pos: QPoint, taskpage):
        super(FavoriteTaskMenu, self).__init__(parent=favoritebox)

        translate_dic = {'fr': ["Supprimer la liste de tâches sélectionné", "Supprimer la liste de tâches sélectionné des favoris",
                                "Confirmer la suppression des favoris", "Voulez-vous retirer", "des favoris?", "Oui",
                                "Non", "Confirmer la suppression", "Voulez-vous supprimer la liste de tâches"],
                         'en': ["Delete selected task list", "Remove selected task list from favorite",
                                "Remove from favorite confirmation", "Do you want to remove", "from favorite?", "Yes",
                                "No", "Delete confirmation", "Do you want to delete task list"]}

        self.ui = mainpage.ui

        self.remove_action = None
        self.remove_favorite_action = None

        # On n'ajoute l'option de supression ou d'ajout aux favoris que s'il y a un élément sélectionné
        current_index = self.ui.followedtask_box.currentIndex()
        if current_index != -1:
            self.remove_action = self.addAction(translate_dic[self.ui.current_lang][0])
            self.remove_favorite_action = self.addAction(translate_dic[self.ui.current_lang][1])

        action = self.exec(self.ui.followedtask_box.mapToGlobal(pos))

        # supression d'un élément des favoris
        if action == self.remove_favorite_action:
            item_text = self.ui.followedtask_box.currentText()

            msg = QMessageBox(taskpage)
            msg.setWindowTitle(translate_dic[self.ui.current_lang][2])
            msg.setText(
                f"{translate_dic[self.ui.current_lang][3]} « {item_text} » {translate_dic[self.ui.current_lang][4]}")

            btn_oui = msg.addButton(translate_dic[self.ui.current_lang][5], QMessageBox.ButtonRole.YesRole)
            btn_non = msg.addButton(translate_dic[self.ui.current_lang][6], QMessageBox.ButtonRole.NoRole)

            msg.exec()

            if msg.clickedButton() == btn_oui:
                self.ui.followedtask_box.removeItem(current_index)

        # supression d'un agenda via la liste des favoris
        elif action == self.remove_action:
            item_text = self.ui.followedtask_box.currentText()

            msg = QMessageBox(taskpage)
            msg.setWindowTitle(translate_dic[self.ui.current_lang][7])
            msg.setText(f"{translate_dic[self.ui.current_lang][8]} « {item_text} » ?")

            btn_oui = msg.addButton(translate_dic[self.ui.current_lang][5], QMessageBox.ButtonRole.YesRole)
            btn_non = msg.addButton(translate_dic[self.ui.current_lang][6], QMessageBox.ButtonRole.NoRole)

            msg.exec()

            if msg.clickedButton() == btn_oui:
                self.ui.mytask_box.removeItem(self.ui.mytask_box.findText(item_text))  # suppression des tâches en récupérant son indice à l'aide de son nom
                self.ui.followedtask_box.removeItem(current_index)  # suppression des favoris