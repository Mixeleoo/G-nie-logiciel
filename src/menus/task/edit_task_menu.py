# Import bibliothèques
from PyQt6.QtCore import QDate, QTime
from PyQt6.QtWidgets import QListWidgetItem, QListWidget
from datetime import datetime

import src.DAO as DAO
# Nos imports
from src.menus.task.task_menuABC import TaskMenuABC
from src.dataclass.task import Task, Color

def int_to_hexcolor(color: Color) -> str:
    return f"#{color.r:02X}{color.g:02X}{color.b:02X}"

class EditTaskMenu(TaskMenuABC):
    def __init__(self, mainpage, taskpage: QListWidget, item: QListWidgetItem):
        '''
       Permet la modification d'une tâche déjà existante
       '''
        super().__init__(mainpage, taskpage)

        if self.ui.current_lang == 'fr':
            self.setWindowTitle("Modifier tâche")
        else:
            self.setWindowTitle("Edit Task")

        self.task: Task = DAO.ogtasklist[taskpage.row(item)]

        # 1. Convertir en datetime standard Python
        dt = datetime.fromtimestamp(self.task.date)

        self.task_name.setText(self.task.name)
        self.date_task.setDate(QDate(dt.year, dt.month, dt.day))
        self.time_task.setTime(QTime(dt.hour, dt.minute, dt.second))
        self.task_details.setText(self.task.details)
        
        self.color_task.setCurrentIndex(
            next((index for index, hexcolor in enumerate(self.colors.values()) if
                    hexcolor == int_to_hexcolor(self.task.color).lower()), 0)
        )
