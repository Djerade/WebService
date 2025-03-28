from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from .config import Config

# Initialisation des extensions
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisation des extensions avec l'application
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Enregistrement des blueprints
    from .controllers.product_controller import product_bp
    app.register_blueprint(product_bp)

    return app 