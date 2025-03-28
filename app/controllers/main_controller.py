from flask import Blueprint, render_template
from flask_login import login_required
from app.models.product import Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
@login_required
def home():
    # Récupérer les derniers produits ajoutés
    latest_products = Product.query.order_by(Product.created_at.desc()).limit(4).all()
    return render_template('home.html', latest_products=latest_products) 