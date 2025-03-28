from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.models.product import Product
from app.forms.product_form import ProductForm
from app import db
import os
import uuid

product_bp = Blueprint('product', __name__)

def save_image(image_file):
    if not image_file:
        return None
    
    # Créer le dossier uploads s'il n'existe pas
    uploads_dir = os.path.join(current_app.static_folder, 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    # Générer un nom de fichier unique
    filename = str(uuid.uuid4()) + secure_filename(image_file.filename)
    file_path = os.path.join(uploads_dir, filename)
    
    # Sauvegarder l'image
    image_file.save(file_path)
    return filename

def delete_image(filename):
    if filename:
        file_path = os.path.join(current_app.static_folder, 'uploads', filename)
        if os.path.exists(file_path):
            os.remove(file_path)

@product_bp.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('products/list.html', products=products)

@product_bp.route('/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        image_filename = save_image(form.image.data)
        
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            image_filename=image_filename
        )
        db.session.add(product)
        db.session.commit()
        flash('Produit créé avec succès!', 'success')
        return redirect(url_for('product.list_products'))
    return render_template('products/create.html', form=form)

@product_bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        if form.image.data:
            # Supprimer l'ancienne image
            delete_image(product.image_filename)
            # Sauvegarder la nouvelle image
            image_filename = save_image(form.image.data)
            product.image_filename = image_filename
            
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        
        db.session.commit()
        flash('Produit mis à jour avec succès!', 'success')
        return redirect(url_for('product.list_products'))
    return render_template('products/edit.html', form=form, product=product)

@product_bp.route('/products/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    
    # Supprimer l'image associée
    delete_image(product.image_filename)
    
    db.session.delete(product)
    db.session.commit()
    flash('Produit supprimé avec succès!', 'success')
    return redirect(url_for('product.list_products')) 