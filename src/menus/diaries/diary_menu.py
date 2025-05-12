from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QInputDialog, QMessageBox, QComboBox
import src.DAO as DAO
from src.dataclass.agenda import Agenda
from src.dataclass.user import User
from src.menus.diaries.diary_menuABC import DiaryMenuABC


class DiaryMenu(DiaryMenuABC) :
    def __init__(self, agendabox, mainpage, pos : QPoint, eventpage) :
        '''
        Gestion des actions possibles sur un agenda
        '''
        super().__init__(agendabox, mainpage)

        self.share_input = None

        self.add_action = self.addAction(self.phrase[0])
        self.edit_action = None
        self.share_action = None

        self.check(pos, eventpage)

        if self.action == self.add_action:
            text, ok = QInputDialog.getText(self, self.phrase[4], self.phrase[5])
            if ok and text:
                DAO.agendalist.append(
                    DAO.agendadao.insert(
                        DAO.user, Agenda(
                            name=text
                        )
                    )
                )
                self.ui.myagenda_box.addItem(text)

        elif self.action == self.edit_action:
            text, ok = QInputDialog.getText(self, self.phrase[18], self.phrase[5])
            if ok and text:
                agenda: Agenda = self.agenda_selected
                agenda.name = text
                DAO.agendadao.update(agenda)

                self.ui.myagenda_box.setItemText(self.ui.myagenda_box.currentIndex(), text)

        elif self.action == self.share_action:
            text, ok = QInputDialog.getText(self, self.phrase[14], self.phrase[15])
            if ok :
                if not text or (text and not DAO.userdao.is_valid(User(mail=text))):
                    error_message = QMessageBox(self.parent())
                    error_message.setWindowTitle(self.phrase[16])
                    error_message.setText(f"{self.phrase[17]}")

                    error_message.setStandardButtons(QMessageBox.StandardButton.Ok)
                    error_message.exec()

                else:
                    DAO.agendadao.share(text, DAO.agendalist[self.ui.myagenda_box.currentIndex()])
    
    def initActions(self) -> None:
        self.edit_action = self.addAction(self.phrase[3])
        self.share_action = self.addAction(self.phrase[13])

    def on_remove(self) -> None:
        self.ui.followedagenda_box.removeItem(self.ui.followedagenda_box.findText(self.item_text))  # suppression des agenda en récupérant son indice à l'aide de son nom
        self.ui.myagenda_box.removeItem(self.current_index) # suppression de l'agenda sélectionné
        
        # suppression de l'agenda dans la base de données
        DAO.agendadao.delete(self.agenda_selected)
        DAO.agendalist.remove(self.agenda_selected)

    @property
    def agendabox(self) -> QComboBox:
        return self.ui.myagenda_box

    @property
    def agendalist(self) -> list[Agenda]:
        return DAO.agendalist

    @property
    def translate_dic(self) -> dict:
        return {
            'fr': [
                "Ajouter un agenda",
                "Supprimer l'agenda sélectionné",
                "Ajouter l'agenda sélectionné aux favoris",
                "Modifier l'agenda sélectionné",
                "Ajouter un agenda",
                "Nom de l'agenda :",
                "Confirmer l'ajout aux favoris",
                "Voulez-vous ajouter",
                "aux favoris?",
                "Oui",
                "Non",
                "Confirmer la suppression",
                "Voulez-vous supprimer",
                "Partager l'agenda sélectionné",
                "Email du receveur",
                "Partager agenda",
                "Erreur email",
                "Entrée non valide",
                "Modifier agenda"
            ],
            'en': [
                "Add a diary",
                "Delete selected diary",
                "Add selected diary to favorite",
                "Edit selected diary",
                "Add a diary",
                "Diary name :",
                "Add to favorite confirmation",
                "Do you want to add",
                "to favorite?",
                "Yes",
                "No",
                "Delete confirmation",
                "Do you want to delete",
                "Share selected diary",
                "Receiver's email",
                "Share diary",
                "Email error",
                "No valide entry",
                "Edit diary"
            ]
        }

    @property
    def title_remove_page(self) -> str:
        return self.phrase[11]

    @property
    def text_remove_page(self) -> str:
        return self.phrase[12]

    @property
    def remove_yes_text(self) -> str:
        return self.phrase[9]

    @property
    def remove_no_text(self) -> str:
        return self.phrase[10]

    @property
    def remove_text(self) -> str:
        return self.phrase[1]