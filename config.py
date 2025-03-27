# config.py
class Config:
    """Configuration centralisée de l'application"""
    # Configuration MongoDB
    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://djeradegolbeparfait:<db_password>@cluster0.yddqr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0',
        'connect': False  # Ne pas se connecter automatiquement
    }
    
    # Clé secrète pour les sessions et autres fonctionnalités sécurisées
    SECRET_KEY = 'votre_clé_secrète_tres_complexe_et_unique'
    
    # Paramètres d'application
    DEBUG = True
    TESTING = False

    # Configuration spécifique à l'environnement
    @classmethod
    def get_config(cls):
        """Permet de surcharger la configuration par environnement"""
        return cls

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    
    # Surcharger avec des paramètres de production
    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://<production_username>:<production_password>@<production_cluster>.mongodb.net/prodatabase',
        'connect': False
    }
    SECRET_KEY = 'une_clé_secrète_de_production_encore_plus_complexe'

class TestingConfig(Config):
    """Configuration pour les tests"""
    TESTING = True
    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost:27017/testdatabase',
        'connect': False
    }
