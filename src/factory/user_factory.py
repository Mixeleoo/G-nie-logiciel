from src.dataclass import User
from src.DAO import UserDAO

class UserFactory:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def create_empty_user(self) -> User:
        """Crée un utilisateur par défaut vide (ex : pour un formulaire)."""
        return User()

    def create_user(self, mail: str, mdp: str) -> User:
        """Crée un utilisateur local (non connecté)."""
        return User(mail=mail, mdp=mdp)

    def register_user(self, mail: str, mdp: str) -> User:
        """
        Crée un utilisateur et le pousse vers le serveur.
        Retourne l'utilisateur avec son ID mis à jour si succès.
        """
        user = self.create_user(mail, mdp)
        response = self.dao.insert(user)
        if response["op"] == 4:  # succès
            user.id = response["data"]["id"]
            return user
        elif response["op"] == 5:  # erreur
            raise ValueError(f"Erreur lors de la création : {response['errmsg']}")
        else:
            raise RuntimeError("Réponse inattendue du serveur")

    def login_user(self, mail: str, mdp: str) -> User:
        """
        Tente de connecter un utilisateur. Retourne l'objet avec ID si succès.
        """
        user = self.create_user(mail, mdp)
        result = self.dao.connect(user)
        if user.id == -1:
            raise PermissionError("Connexion échouée : identifiants invalides")
        return user

    def is_existing_user(self, mail: str) -> bool:
        """Vérifie si un utilisateur existe (pour l’inscription par exemple)."""
        return self.dao.is_valid(User(mail=mail))
