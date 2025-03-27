from flask import Flask
import os
from dotenv import load_dotenv # type: ignore
from .config import mongo
from config import DevelopmentConfig, ProductionConfig, TestingConfig
# load_dotenv()  # Charger les variables d'environnement
from .views.user_views import user_bp

def create_app():
    app = Flask(__name__)
    
    # Configuration MongoDB
    app.config['MONGO_URI'] = os.getenv('MONGODB_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Initialiser MongoDB
    mongo.init_app(app)
    
    # Importer et enregistrer les blueprints
   
    app.register_blueprint(user_bp)
    
    return app