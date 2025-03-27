from flask import Flask
import os
# from dotenv import load_dotenv
from .database import mongo

# load_dotenv()  # Charger les variables d'environnement

def create_app():
    app = Flask(__name__)
    
    # Configuration MongoDB
    app.config['MONGO_URI'] = os.getenv('MONGODB_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Initialiser MongoDB
    mongo.init_app(app)
    
    # Importer et enregistrer les blueprints
    from .views.user_views import user_bp
    app.register_blueprint(user_bp)
    
    return app