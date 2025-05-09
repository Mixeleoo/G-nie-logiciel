from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QMenu, QMessageBox
import src.DAO as DAO
from src.dataclass.agenda import Agenda

class SharedDiaryMenu(QMenu):
    def __init__(self, favoritebox, mainpage, pos : QPoint, eventpage) :
        super(SharedDiaryMenu, self).__init__(parent = favoritebox)

        translate_dic = {'fr' : ["Supprimer l'agenda sélectionné","Supprimer l'agenda sélectionné des favoris","Confirmer la suppression des favoris","Voulez-vous retirer","des favoris?","Oui","Non","Confirmer la suppression","Voulez-vous supprimer l'agenda"],
                         'en' : ["Delete selected diary","Remove selected diary from favorite","Remove from favorite confirmation","Do you want to remove","from favorite?","Yes","No","Delete confirmation","Do you want to delete diary"]}
        
        self.ui = mainpage.ui

        self.remove_action = None

        # On n'ajoute l'option de supression ou d'ajout aux favoris que s'il y a un élément sélectionné
        current_index = self.ui.followedagenda_box.currentIndex()
        if current_index != -1:
            self.remove_action = self.addAction(translate_dic[self.ui.current_lang][0])

        action = self.exec(self.ui.followedagenda_box.mapToGlobal(pos))

        # supression d'un agenda suivi
        if action == self.remove_action:
            item_text = self.ui.followedagenda_box.currentText()

            msg = QMessageBox(eventpage)
            msg.setWindowTitle(translate_dic[self.ui.current_lang][7])
            msg.setText(f"{translate_dic[self.ui.current_lang][8]} « {item_text} » ?")

            btn_oui = msg.addButton(translate_dic[self.ui.current_lang][5], QMessageBox.ButtonRole.YesRole)
            btn_non = msg.addButton(translate_dic[self.ui.current_lang][6], QMessageBox.ButtonRole.NoRole)

            msg.exec()

            if msg.clickedButton() == btn_oui:
                self.ui.followedagenda_box.removeItem(current_index)  # suppression des favoris
                DAO.agendadao.delete_shared_agenda(DAO.user, self.selected_agenda)

    @property
    def selected_agenda(self) -> Agenda:
        return DAO.sharedagendalist[self.ui.followedagenda_box.currentIndex()]
