from PyQt6.QtCore import QPoint, QTimer
from PyQt6.QtWidgets import QMenu, QInputDialog, QMessageBox, QDialog, QLineEdit, QLabel
import src.DAO as DAO
from src.dataclass import Agenda, User

translate_dic = {
    'fr': ["Ajouter un agenda", "Supprimer l'agenda sélectionné", "Ajouter l'agenda sélectionné aux favoris",
           "Modifier l'agenda sélectionné", "Ajouter un agenda", "Nom de l'agenda :", "Confirmer l'ajout aux favoris",
           "Voulez-vous ajouter", "aux favoris?", "Oui", "Non", "Confirmer la suppression", "Voulez-vous supprimer",
           "Partager l'agenda sélectionné","Email du receveur","Partager agenda","Erreur email","Entrée non valide","Modifier agenda"],
    'en': ["Add a diary", "Delete selected diary", "Add selected diary to favorite", "Edit selected diary",
           "Add a diary", "Diary name :", "Add to favorite confirmation", "Do you want to add", "to favorite?", "Yes",
           "No", "Delete confirmation", "Do you want to delete", "Share selected diary","Receiver's email","Share diary","Email error","No valide entry","Edit diary"]}



class DiaryMenu(QMenu) :

    @property
    def phrase(self) -> list[str]:
        return translate_dic[self.ui.current_lang]
    
    @property
    def agenda_selected(self) -> Agenda:
        return DAO.agendalist[self.ui.myagenda_box.currentIndex()]
    
    def __init__(self, agandabox, mainpage, pos : QPoint, eventpage) :
        super().__init__(parent = agandabox)
        self.ui = mainpage.ui

        self.share_input = None

        self.add_action = self.addAction(self.phrase[0])
        self.edit_action = None
        self.remove_action = None
        self.favorite_action = None
        self.share_action = None

        current_index = self.ui.myagenda_box.currentIndex()
        if current_index != -1:
            self.favorite_action = self.addAction(self.phrase[2])
            self.remove_action = self.addAction(self.phrase[1])
            self.edit_action = self.addAction(self.phrase[3])
            self.share_action = self.addAction(self.phrase[13])

        action = self.exec(self.ui.myagenda_box.mapToGlobal(pos))

        if action == self.add_action:
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

        elif action == self.edit_action:
            text, ok = QInputDialog.getText(self, self.phrase[18], self.phrase[5])
            if ok and text:
                agenda: Agenda = self.agenda_selected
                agenda.name = text
                DAO.agendadao.update(agenda)

                self.ui.myagenda_box.setItemText(self.ui.myagenda_box.currentIndex(), text)

        elif action == self.favorite_action:
            # TODO Léo: Mémoriser ces ajouts quelque pars
            item_text = self.ui.myagenda_box.currentText()

            msg = QMessageBox(eventpage)
            msg.setWindowTitle(self.phrase[6])
            msg.setText(f"{self.phrase[7]} « {item_text} » {self.phrase[8]}")

            btn_oui = msg.addButton(self.phrase[9], QMessageBox.ButtonRole.YesRole)
            btn_non = msg.addButton(self.phrase[10], QMessageBox.ButtonRole.NoRole)

            msg.exec()

            if msg.clickedButton() == btn_oui:
                self.ui.followedagenda_box.addItem(item_text)

        elif action == self.remove_action:
            item_text = self.ui.myagenda_box.currentText()

            msg = QMessageBox(eventpage)
            msg.setWindowTitle(self.phrase[11])
            msg.setText(f"{self.phrase[12]} « {item_text} » ?")

            btn_oui = msg.addButton(self.phrase[9], QMessageBox.ButtonRole.YesRole)
            btn_non = msg.addButton(self.phrase[10], QMessageBox.ButtonRole.NoRole)

            msg.exec()

            if msg.clickedButton() == btn_oui:
                self.ui.followedagenda_box.removeItem(self.ui.followedagenda_box.findText(item_text))  # suppression des agenda en récupérant son indice à l'aide de son nom
                self.ui.myagenda_box.removeItem(current_index) # suppression de l'agenda sélectionné
                
                # suppression de l'agenda dans la base de données
                DAO.agendadao.delete(self.agenda_selected)

        elif action == self.share_action:
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
