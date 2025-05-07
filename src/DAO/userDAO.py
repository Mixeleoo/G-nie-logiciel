
from src.dbcom import DBCom, dbcom
from src.dataclass.user import User

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
        if m_json["op"] == 5:
            user.id = -1
        else:
            user.id = m_json["data"]["id"]
        return user

    def update(self, user: User):
        pass

    def is_valid(self, user: User) -> bool:
        self.dbcom.sendall({
            "data":{
                "mail": user.mail,
            },
            "requestType": "isUserValid",
            "op": 3
        })
        m_json = self.dbcom.recv()
        return m_json["op"] == 4 and m_json["data"]["is_valid"]

userdao = UserDAO(dbcom)
user = User()
