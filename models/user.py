# from marshmallow import Schema, fields, validate, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
# from bson.objectid import ObjectId
import re

class UserSchema(Schema):
    """Schéma de validation pour les utilisateurs"""
    username = fields.Str(
        required=True, 
        validate=[
            validate.Length(min=3, max=50, 
            error="Le nom d'utilisateur doit avoir entre 3 et 50 caractères")
        ]
    )
    email = fields.Email(
        required=True, 
        validate=[validate.Email(error="Email invalide")]
    )
    password = fields.Str(
        required=True,
        validate=[validate.Length(min=6, error="Le mot de passe doit avoir au moins 6 caractères")]
    )
    bio = fields.Str(allow_none=True, validate=validate.Length(max=500))

class User:
    """Modèle de gestion des utilisateurs"""
    def __init__(self, mongo_client):
        self.db = mongo_client.get_database()
        self.collection = self.db.users
        self.schema = UserSchema()
    
    def create_user(self, user_data):
        """Créer un nouvel utilisateur"""
        try:
            # Valider les données
            validated_data = self.schema.load(user_data)
            
            # Vérifier si l'utilisateur existe déjà
            existing_user = self.collection.find_one({
                '$or': [
                    {'username': validated_data['username']},
                    {'email': validated_data['email']}
                ]
            })
            
            if existing_user:
                raise ValueError("Un utilisateur avec ce nom ou email existe déjà")
            
            # Hasher le mot de passe
            validated_data['password'] = generate_password_hash(
                validated_data['password']
            )
            
            # Insérer l'utilisateur
            result = self.collection.insert_one(validated_data)
            
            # Récupérer l'utilisateur inséré
            return self.get_user_by_id(result.inserted_id)
        
        except ValidationError as err:
            raise ValueError(err.messages)
    
    def get_user_by_id(self, user_id):
        """Récupérer un utilisateur par son ID"""
        user = self.collection.find_one({'_id': ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
            del user['password']  # Ne jamais renvoyer le mot de passe
            return user
        return None
    
    def authenticate_user(self, email, password):
        """Authentifier un utilisateur"""
        user = self.collection.find_one({'email': email})
        
        if user and check_password_hash(user['password'], password):
            # Convertir l'ObjectId en string et supprimer le mot de passe
            user['_id'] = str(user['_id'])
            del user['password']
            return user
        
        return None
    
    def list_users(self):
        """Lister tous les utilisateurs"""
        users = list(self.collection.find())
        for user in users:
            user['_id'] = str(user['_id'])
            del user['password']
        return users
