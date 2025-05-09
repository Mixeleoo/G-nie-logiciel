
# Import bibliothèques
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QColor
from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel, QDateEdit, QTimeEdit, QPushButton, QComboBox, QListWidgetItem
from datetime import datetime

# Nos import
from src.menus.event.event_list_menu import EventListMenu

import src.DAO as DAO
from src.dataclass.event import Event, Color
from src.menus.event.event_menuABC import EventMenuABC

def int_to_hexcolor(color: Color) -> str:
    return f"#{color.r:02X}{color.g:02X}{color.b:02X}"

class EditEventMenu(EventMenuABC) :
    def __init__(self, mainpage, eventpage: EventListMenu, item: QListWidgetItem):
        super().__init__(mainpage, eventpage)

        self.event: Event = eventpage.get_event_selected(item)
        self.event_name.setText(self.event.name)

        # 1. Convertir en datetime standard Python
        dt = datetime.fromtimestamp(self.event.start)

        self.date_event.setDate(QDate(dt.year, dt.month, dt.day))
        self.time_event.setTime(QTime(dt.hour, dt.minute, dt.second))

        # TODO Léo :self.new_location.setText()
        self.agenda_event.setCurrentText(
            next((agenda.name for agenda in DAO.agendalist if (agenda.id == self.event.agenda_id)), "WAZAZA")
        )

        self.color_event.setCurrentIndex(
            next((index for index, hexcolor in enumerate(self.colors.values()) if
                    hexcolor == int_to_hexcolor(self.event.color).lower()), 0)
        )

        if self.ui.current_lang == "fr":
            self.setWindowTitle("Modifier évenement")
        else:
            self.setWindowTitle("Edit event")
        