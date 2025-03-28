from app import create_app, db
from app.models.product import Product
from app.models.user import User

def init_db():
    app = create_app()
    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        print("Base de données initialisée avec succès!")

if __name__ == '__main__':
    init_db() 