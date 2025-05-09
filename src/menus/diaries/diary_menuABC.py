from PyQt6.QtCore import QPoint, QTimer
from PyQt6.QtWidgets import QMenu, QComboBox, QMessageBox
import src.DAO as DAO
from src.dataclass.agenda import Agenda
from src.dataclass.user import User
from abc import abstractmethod


class DiaryMenuABC(QMenu):
    def __init__(self, agendabox, mainpage):
        super().__init__(parent=agendabox)

        self.ui = mainpage.ui
        self.remove_action = None
        self.item_text = ""

    def check(self, pos, eventpage):
        self.current_index = self.agendabox.currentIndex()
        
        if self.current_index != -1:
            self.initActions()
            self.remove_action = self.addAction(self.remove_text)

        self.action = self.exec(self.agendabox.mapToGlobal(pos))

        if self.action == self.remove_action:
            self.item_text = self.agendabox.currentText()

            msg = QMessageBox(eventpage)
            msg.setWindowTitle(self.title_remove_page)
            msg.setText(f"{self.text_remove_page} « {self.item_text} » ?")

            btn_oui = msg.addButton(self.remove_yes_text, QMessageBox.ButtonRole.YesRole)
            msg.addButton(self.remove_no_text, QMessageBox.ButtonRole.NoRole)

            msg.exec()

            if msg.clickedButton() == btn_oui:
                self.on_remove()

    @abstractmethod
    def initActions(self) -> None:
        pass

    @abstractmethod
    def on_remove(self) -> None:
        pass

    @property
    @abstractmethod
    def remove_text(self) -> str:
        pass

    @property
    @abstractmethod
    def remove_yes_text(self) -> str:
        pass

    @property
    @abstractmethod
    def remove_no_text(self) -> str:
        pass

    @property
    @abstractmethod
    def title_remove_page(self) -> str:
        pass

    @property
    @abstractmethod
    def text_remove_page(self) -> str:
        pass
    
    @property
    @abstractmethod
    def translate_dic(self) -> dict:
        pass

    @property
    @abstractmethod
    def agendabox(self) -> QComboBox:
        pass

    @property
    @abstractmethod
    def agendalist(self) -> list[Agenda]:
        pass

    @property
    def agenda_selected(self) -> Agenda:
        return self.agendalist[self.agendabox.currentIndex()]

    @property
    def phrase(self) -> list[str]:
        return self.translate_dic[self.ui.current_lang]
