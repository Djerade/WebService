# app/controllers/product_controller.py
from app.models.product import Product
from app import db
from werkzeug.utils import secure_filename
import os

class ProductController:
    @staticmethod
    def get_all_products(category=None):
        """
        Récupère tous les produits, avec un filtrage optionnel par catégorie
        """
        if category:
            return Product.query.filter_by(category=category).all()
        return Product.query.all()

    @staticmethod
    def get_product_by_id(product_id):
        """
        Récupère un produit par son ID
        """
        return Product.query.get_or_404(product_id)
    
    @staticmethod
    def create_product(form, current_user, upload_folder):
        """
        Crée un nouveau produit
        """
        # Gestion de l'upload d'image
        image_filename = None
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            image_path = os.path.join(upload_folder, filename)
            file.save(image_path)
            image_filename = filename

        # Création du produit
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            quantity=form.quantity.data,
            category=form.category.data,
            image=image_filename,
            farmer=current_user
        )
        
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def update_product(product_id, form):
        """
        Met à jour un produit existant
        """
        product = Product.query.get_or_404(product_id)
        
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        product.category = form.category.data
        
        # Gestion de l'image si un nouveau fichier est téléchargé
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            image_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(image_path)
            product.image = filename
        
        db.session.commit()
        return product

    @staticmethod
    def delete_product(product_id):
        """
        Supprime un produit
        """
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()

    @staticmethod
    def search_products(query):
        """
        Recherche de produits par nom ou description
        """
        return Product.query.filter(
            (Product.name.ilike(f'%{query}%')) | 
            (Product.description.ilike(f'%{query}%'))
        ).all()