from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QMenu, QInputDialog, QMessageBox


class DiaryMenu(QMenu) :
    def __init__(self, agandabox, mainpage, pos : QPoint, eventpage) :
        super().__init__(parent = agandabox)
        self.ui = mainpage.ui

        translate_dic = {'fr' : ["Ajouter un agenda","Supprimer l'agenda sélectionné","Ajouter l'agenda sélectionné aux favoris","Modifier l'agenda sélectionné","Ajouter un agenda","Nom de l'agenda :","Confirmer l'ajout aux favoris","Voulez-vous ajouter","aux favoris?","Oui","Non","Confirmer la suppression","Voulez-vous supprimer"],
                         'en' : ["Add a diary","Delete selected diary","Add selected diary to favorite","Edit selected diary","Add a diary","Diary name :","Add to favorite confirmation","Do you want to add","to favorite?","Yes","No","Delete confirmation","Do you want to delete"]}

        self.add_action = self.addAction(translate_dic[self.ui.current_lang][0])
        self.edit_action = None
        self.remove_action = None
        self.favorite_action = None

        current_index = self.ui.myagenda_box.currentIndex()
        if current_index != -1:
            self.favorite_action = self.addAction(translate_dic[self.ui.current_lang][2])
            self.remove_action = self.addAction(translate_dic[self.ui.current_lang][1])
            self.edit_action = self.addAction(translate_dic[self.ui.current_lang][3])

        action = self.exec(self.ui.myagenda_box.mapToGlobal(pos))

        if action == self.add_action:
            text, ok = QInputDialog.getText(self, translate_dic[self.ui.current_lang][4], translate_dic[self.ui.current_lang][5])
            if ok and text:
                self.ui.myagenda_box.addItem(text)

        elif action == self.favorite_action:
            item_text = self.ui.myagenda_box.currentText()

            msg = QMessageBox(eventpage)
            msg.setWindowTitle(translate_dic[self.ui.current_lang][6])
            msg.setText(f"{translate_dic[self.ui.current_lang][7]} « {item_text} » {translate_dic[self.ui.current_lang][8]}")

            btn_oui = msg.addButton(translate_dic[self.ui.current_lang][9], QMessageBox.ButtonRole.YesRole)
            btn_non = msg.addButton(translate_dic[self.ui.current_lang][10], QMessageBox.ButtonRole.NoRole)

            msg.exec()

            if msg.clickedButton() == btn_oui:
                self.ui.followedagenda_box.addItem(item_text)

        elif action == self.remove_action:
            item_text = self.ui.myagenda_box.currentText()

            msg = QMessageBox(eventpage)
            msg.setWindowTitle(translate_dic[self.ui.current_lang][11])
            msg.setText(f"{translate_dic[self.ui.current_lang][12]} « {item_text} » ?")

            btn_oui = msg.addButton(translate_dic[self.ui.current_lang][9], QMessageBox.ButtonRole.YesRole)
            btn_non = msg.addButton(translate_dic[self.ui.current_lang][10], QMessageBox.ButtonRole.NoRole)

            msg.exec()

            if msg.clickedButton() == btn_oui:
                self.ui.followedagenda_box.removeItem(self.ui.followedagenda_box.findText(item_text))  # suppression des agenda en récupérant son indice à l'aide de son nom
                self.ui.myagenda_box.removeItem(current_index) # suppression de l'agenda sélectionné