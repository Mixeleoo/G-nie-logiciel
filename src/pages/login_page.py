from PyQt6.QtWidgets import QWidget

from src.main import MainWindow
import src.DAO as DAO
from src.dataclass.user import User
from src.menus.task.task_display import TaskFinishedDisplay, TaskOngoingDisplay

class LoginPage(QWidget):
    def __init__(self, mainpage: MainWindow):
        '''
        Initialise la page d'acceuil du logiciel
        '''
        super().__init__(mainpage)
        self.ui = mainpage.ui
        self.mainpage = mainpage

        self.ui.back_button.clicked.connect(lambda : self.goto_homepage()) # bouton retour
        self.ui.validate_connect_button.clicked.connect(self.validate_connection)

        # supression du message d'erreur
        self.ui.error_label1.hide()
        self.ui.email_line_connection.textEdited.connect(lambda : self.clear_error())
        self.ui.password_line_connection.textEdited.connect(lambda : self.clear_error())

    def goto_homepage(self):
        '''
        Change la page du logiciel à la page d'acceuil
        :return: None
        '''
        self.ui.pages_logiciel.setCurrentIndex(0) # homepage
        self.ui.error_label1.hide() #suppression du message d'erreur
        self.clear_all()

    def clear_all(self):
        self.ui.email_line_connection.clear()
        self.ui.password_line_connection.clear()

    def validate_connection(self):
        '''
        Connecte l'utilisateur si son identifiant et mot de passe sont corrects
        :return: None
        '''
        if self.check_connection():
            # Si la connexion est validée, alors on va chopper la liste de ses agendas
            DAO.agendalist = DAO.agendadao.get_list(DAO.user)
            DAO.pendingsharedagendalist = DAO.agendadao.get_pending_agenda_list(DAO.user)
            DAO.sharedagendalist = DAO.agendadao.get_shared_agenda_list(DAO.user)

            # Récupérer toutes les tâches de l'utilisateur
            for task in DAO.taskdao.get_task_list(DAO.user):
                if task.done:
                    DAO.ftasklist.append(task)
                else:
                    DAO.ogtasklist.append(task)

            # ajout des agendas de l'utilisateur
            for agenda in DAO.agendalist:
                self.ui.myagenda_box.addItem(agenda.name)

            # remplissage de la liste des agendas suivis
            for agenda in DAO.sharedagendalist:
                self.ui.followedagenda_box.addItem(agenda.name)

            text: str = self.ui.email_label_e.text()
            self.ui.email_label_e.setText(text + " " + DAO.user.mail)
            text: str = self.ui.email_label_t.text()
            self.ui.email_label_t.setText(text + " " + DAO.user.mail)
                
            self.ui.pages_logiciel.setCurrentIndex(3) #aller à la pages evenement
            self.clear_all()

            self.ui.ongoing_task_display = TaskOngoingDisplay(self.mainpage, self.ui.frame_task)
            self.ui.finished_task_display = self.finished_task = TaskFinishedDisplay(self.mainpage, self.ui.frame_7)
        else :
            self.ui.error_label1.show()

    def clear_error(self):
        '''
        Enlève l'affichage de l'erreur quand l'utlisateur recommence à taper dans les input
        :return: None
        '''
        self.ui.error_label1.hide() # suppression du message d'erreur

    def check_connection(self) -> bool:
        '''
        Verifie que l'identifiant et mot de passe tapé par l'utilisateur sont correct
        :return: retourne True si correct et False sinon
        '''

        # La fonction retourne un user dont l'id est -1 si le compte existe, sinon l'id du compte
        DAO.user = DAO.userdao.connect(
            User(
                mail=self.ui.email_line_connection.text(),
                mdp=self.ui.password_line_connection.text()
            )
        )

        return DAO.user.id != -1
