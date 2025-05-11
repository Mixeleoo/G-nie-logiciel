from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QMenu, QMessageBox, QComboBox
import src.DAO as DAO
from src.dataclass.agenda import Agenda
from src.menus.diaries.diary_menuABC import DiaryMenuABC

       
class SharedDiaryMenu(DiaryMenuABC):
    def __init__(self, favoritebox, mainpage, pos : QPoint, eventpage) :
        '''
        Gestion des actions possibles sur un agenda partagé
        '''
        super().__init__(favoritebox, mainpage)
        self.check(pos, eventpage)

    def initActions(self) -> None:
        pass
        
    def on_remove(self) -> None:
        self.ui.followedagenda_box.removeItem(self.current_index)  # suppression des favoris
        DAO.agendadao.delete_shared_agenda(DAO.user, self.agenda_selected)

    @property
    def agendabox(self) -> QComboBox:
        return self.ui.followedagenda_box

    @property
    def agendalist(self) -> list[Agenda]:
        return DAO.sharedagendalist
    
    @property
    def translate_dic(self) -> dict:
        return {
            'fr' : [
                "Supprimer l'agenda sélectionné",
                "Supprimer l'agenda sélectionné des favoris",
                "Confirmer la suppression des favoris",
                "Voulez-vous retirer",
                "des favoris?",
                "Oui",
                "Non",
                "Confirmer la suppression",
                "Voulez-vous supprimer l'agenda"
            ],
            'en' : [
                "Delete selected diary",
                "Remove selected diary from favorite",
                "Remove from favorite confirmation",
                "Do you want to remove",
                "from favorite?",
                "Yes",
                "No",
                "Delete confirmation",
                "Do you want to delete diary"
            ]
        }

    @property
    def title_remove_page(self) -> str:
        return self.phrase[7]

    @property
    def text_remove_page(self) -> str:
        return self.phrase[8]

    @property
    def remove_yes_text(self) -> str:
        return self.phrase[5]

    @property
    def remove_no_text(self) -> str:
        return self.phrase[6]

    @property
    def remove_text(self) -> str:
        return self.phrase[0]
    