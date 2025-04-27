
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

    def connect(self, user: User) -> str:
        self.dbcom.sendall({
            "authentification":{
                "mail": user.mail,
                "mdp": user.mdp
            },
            "op": 2
        })
        m_json = self.dbcom.recv()
        user.id = m_json["data"]["id"]
        return user

    def update(self, user: User):
        pass

userdao = UserDAO(dbcom)
