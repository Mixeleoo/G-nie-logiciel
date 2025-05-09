
from src.menus.event.event_menuABC import EventMenuABC

class EventMenu(EventMenuABC):
    def __init__(self, mainpage, eventpage):
        super().__init__(mainpage, eventpage)

        if self.ui.current_lang == "fr":
            self.setWindowTitle("Créer un évenement")

        else:
            self.setWindowTitle("Create event")
        