from app import create_app, db
from app.models.product import Product

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Product': Product}

if __name__ == '__main__':
    with app.app_context():
        # Créer les tables de la base de données si elles n'existent pas
        db.create_all()
    app.run(debug=True) 