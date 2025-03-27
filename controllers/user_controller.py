from ..database import mongo
from ..models.user import User

class UserController:
    def __init__(self):
        self.user_model = User(mongo.cx)
    
    def list_users(self):
        """Récupérer tous les utilisateurs"""
        return self.user_model.list_users()
    
    def create_user(self, user_data):
        """Créer un nouvel utilisateur"""
        return self.user_model.create_user(user_data)
    
    def authenticate_user(self, email, password):
        """Authentifier un utilisateur"""
        return self.user_model.authenticate_user(email, password)