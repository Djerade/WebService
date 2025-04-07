from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.models.message import Message
from app.forms.user_form import LoginForm, RegistrationForm, ProfileForm
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
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Votre compte est désactivé. Veuillez contacter l\'administrateur.', 'error')
                return redirect(url_for('user.login'))
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.home'))
        flash('Email ou mot de passe incorrect.', 'error')
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
            phone_number=form.phone_number.data,
            user_type=form.user_type.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('user.login'))
    
    return render_template('users/register.html', title='Inscription', form=form)

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté avec succès.', 'success')
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

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('Votre profil a été mis à jour avec succès.', 'success')
        return redirect(url_for('user.profile'))
    return render_template('users/profile.html', title='Mon Profil', form=form) 



@user_bp.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
        if not current_user.is_authenticated:
            flash('Vous devez être connecté pour accéder aux messages.', 'danger')
            return redirect(url_for('user.login'))

        if request.method == 'POST':
            recipient_id = request.form.get('recipient_id')
            message_content = request.form.get('message')
            
            if not recipient_id or not message_content:
                flash('Tous les champs sont obligatoires.', 'danger')
                return redirect(url_for('user.messages'))
            
            recipient = User.query.get(recipient_id)
            if not recipient:
                flash('Utilisateur destinataire introuvable.', 'danger')
                return redirect(url_for('user.messages'))
            
            # Créer un nouveau message
            new_message = Message(
                sender_id=current_user.id,
                recipient_id=recipient_id,
                content=message_content,
                timestamp=datetime.utcnow()
            )
            db.session.add(new_message)
            db.session.commit()
            flash('Message envoyé avec succès.', 'success')
            return redirect(url_for('user.messages'))
        
        # Récupérer les messages de l'utilisateur
        sent_messages = Message.query.filter_by(sender_id=current_user.id).all()
        received_messages = Message.query.filter_by(recipient_id=current_user.id).all()
        
        return render_template('users/messages.html',
                               title='Messages',
                               sent_messages=sent_messages,
                               received_messages=received_messages)