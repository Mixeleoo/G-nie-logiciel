
from dbcom import DBCom, dbcom
from dataclass import User

class UserDAO:
    def __init__(self, s: DBCom):
        self.dbcom = s
        
    def insert(self, user: User):
        self.dbcom.sendall({
            "authentification":{
                "mail": user.mail,
                "mdp": user.mdp
            },
            "op": 1
        })
        return self.dbcom.recv()

    def connect(self, user: User) -> User:
        """
        Fonction qui retourne l'user mis en paramètre avec l'id à -1 si le compte existe pas sinon l'id du compte
        :param user: User avec mail et mdp non vides
        :return:
        """
        self.dbcom.sendall({
            "authentification":{
                "mail": user.mail,
                "mdp": user.mdp
            },
            "op": 2
        })
        m_json = self.dbcom.recv()
        if m_json["op"] == 5:
            user.id = -1
        else:
            user.id = m_json["data"]["id"]
        return user

    def update(self, user: User):
        pass

userdao = UserDAO(dbcom)
