
from src.menus.task.task_menuABC import TaskMenuABC

class TaskMenu(TaskMenuABC):
    def __init__(self, mainpage, taskpage):
        '''
       Permet la création d'une nouvelle tâche
       '''
        super().__init__(mainpage, taskpage)

        # fenetre en francais
        if self.ui.current_lang == "fr":
            self.setWindowTitle("Créer une tâche")

        # fenetre en anglais
        elif self.ui.current_lang == "en":
            self.setWindowTitle("Create task")