# Import bibliothèques
from PyQt6.QtCore import QDate, QTime
from PyQt6.QtWidgets import QListWidgetItem
from datetime import datetime

# Nos imports
from src.menus.task.task_menuABC import TaskMenuABC
from src.dataclass.task import Task, Color

def int_to_hexcolor(color: Color) -> str:
    return f"#{color.r:02X}{color.g:02X}{color.b:02X}"

class EditTaskMenu(TaskMenuABC):
    def __init__(self, mainpage, taskpage, item: QListWidgetItem):
        super().__init__(mainpage, taskpage)

        if self.ui.current_lang == 'fr':
            self.setWindowTitle("Modifier tâche")
        else:
            self.setWindowTitle("Edit Task")

        self.task: Task = taskpage.get_event_selected(item)

        # 1. Convertir en datetime standard Python
        dt = datetime.fromtimestamp(self.task.date)

        self.task_name.setText(self.task.name)
        self.new_date.setDate(QDate(dt.year, dt.month, dt.day))
        self.new_hour.setTime(QTime(dt.hour, dt.minute, dt.second))
        self.new_details.setText(self.task.details)
        
        self.color_event.setCurrentIndex(
            next((index for index, hexcolor in enumerate(self.colors.values()) if
                    hexcolor == int_to_hexcolor(self.event.color).lower()), 0)
        )
