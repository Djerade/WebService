from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.forms.user_form import LoginForm, RegistrationForm
from app import db
from datetime import datetime
from app.models.product import Product

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')
            return redirect(url_for('user.login'))
        
        if not user.is_active:
            flash('Votre compte est désactivé. Veuillez contacter l\'administrateur.', 'danger')
            return redirect(url_for('user.login'))
        
        login_user(user, remember=form.remember_me.data)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.home')
        return redirect(next_page)
    
    return render_template('users/login.html', title='Connexion', form=form)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            user_type=form.user_type.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Félicitations, vous êtes maintenant inscrit!', 'success')
        return redirect(url_for('user.login'))
    
    return render_template('users/register.html', title='Inscription', form=form)

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@user_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_vendeur():
        flash('Accès refusé. Cette page est réservée aux vendeurs.', 'danger')
        return redirect(url_for('main.home'))
    
    # Récupérer les statistiques
    total_products = Product.query.count()
    products_in_stock = Product.query.filter(Product.stock > 0).count()
    low_stock_products = Product.query.filter(Product.stock <= 5).count()
    
    # Récupérer les produits récents
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()
    
    return render_template('users/dashboard.html',
                         total_products=total_products,
                         products_in_stock=products_in_stock,
                         low_stock_products=low_stock_products,
                         recent_products=recent_products) 