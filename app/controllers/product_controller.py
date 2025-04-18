from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models.product import Product
from app.forms.product_form import ProductForm
from app import db
import os
import uuid
from functools import wraps

product_bp = Blueprint('product', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

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

def vendeur_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_vendeur():
            flash('Accès refusé. Cette action est réservée aux vendeurs.', 'danger')
            return redirect(url_for('product.list_products'))
        return f(*args, **kwargs)
    return decorated_function

@product_bp.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('products/list.html', products=products)

@product_bp.route('/my-products')
@login_required
@vendeur_required
def my_products():
    products = Product.query.filter_by(seller_id=current_user.id).all()
    return render_template('products/my_products.html', products=products)

@product_bp.route('/product/create', methods=['GET', 'POST'])
@login_required
@vendeur_required
def create_product():
    if not current_user.is_vendeur():
        flash("Accès refusé. Cette action est réservée aux vendeurs.", "error")
        return redirect(url_for("product.list_products"))
    
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            category=form.category.data,
            seller_id=current_user.id
        )
        
        # Gestion de l'image
        if form.image.data:
            file = form.image.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Créer le dossier uploads s'il n'existe pas
                os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
                # Sauvegarder le fichier
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                product.image_path = filename
        
        db.session.add(product)
        db.session.commit()
        flash("Produit créé avec succès !", "success")
        return redirect(url_for("product.list_products"))
    
    return render_template("products/create.html", form=form)

@product_bp.route('/product/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@vendeur_required
def edit_product(id):
    if not current_user.is_vendeur():
        flash("Accès refusé. Cette action est réservée aux vendeurs.", "error")
        return redirect(url_for("product.list_products"))
    
    product = Product.query.get_or_404(id)
    if product.seller_id != current_user.id:
        flash("Vous n'êtes pas autorisé à modifier ce produit.", "error")
        return redirect(url_for("product.list_products"))
    
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.category = form.category.data
        
        # Gestion de l'image
        if form.image.data:
            file = form.image.data
            if file and allowed_file(file.filename):
                # Supprimer l'ancienne image si elle existe
                if product.image_path:
                    old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], product.image_path)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                filename = secure_filename(file.filename)
                # Créer le dossier uploads s'il n'existe pas
                os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
                # Sauvegarder le nouveau fichier
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                product.image_path = filename
        
        db.session.commit()
        flash("Produit mis à jour avec succès !", "success")
        return redirect(url_for("product.list_products"))
    
    return render_template("products/edit.html", form=form, product=product)

@product_bp.route('/product/<int:id>/delete', methods=['POST'])
@login_required
@vendeur_required
def delete_product(id):
    if not current_user.is_vendeur():
        flash("Accès refusé. Cette action est réservée aux vendeurs.", "error")
        return redirect(url_for("product.list_products"))
    
    product = Product.query.get_or_404(id)
    if product.seller_id != current_user.id:
        flash("Vous n'êtes pas autorisé à supprimer ce produit.", "error")
        return redirect(url_for("product.list_products"))
    
    # Supprimer l'image si elle existe
    if product.image_path:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], product.image_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(product)
    db.session.commit()
    flash("Produit supprimé avec succès !", "success")
    return redirect(url_for("product.list_products"))

@product_bp.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('products/detail.html', product=product) 