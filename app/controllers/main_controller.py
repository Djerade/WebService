from flask import Blueprint, render_template
from flask_login import current_user
from app.models.product import Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    latest_products = Product.query.order_by(Product.created_at.desc()).limit(6).all()
    
    if current_user.is_authenticated:
        if current_user.is_vendeur():
            # Statistiques pour les vendeurs
            total_products = Product.query.count()
            products_in_stock = Product.query.filter(Product.stock > 0).count()
            low_stock_products = Product.query.filter(Product.stock <= 5).count()
            
            return render_template('home_vendeur.html',
                                latest_products=latest_products,
                                total_products=total_products,
                                products_in_stock=products_in_stock,
                                low_stock_products=low_stock_products)
        else:
            # Vue pour les clients
            return render_template('home_client.html', latest_products=latest_products)
    else:
        # Vue pour les visiteurs
        return render_template('home_visitor.html', latest_products=latest_products) 