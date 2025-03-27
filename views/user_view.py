from flask import Blueprint, request, jsonify, render_template
from ..controllers.user_controller import UserController

user_bp = Blueprint('users', __name__)
user_controller = UserController()

@user_bp.route('/users', methods=['GET'])
def list_users():
    """Liste tous les utilisateurs"""
    users = user_controller.list_users()
    return render_template('users/list.html', users=users)

@user_bp.route('/users/register', methods=['GET', 'POST'])
def register():
    """Enregistrer un nouvel utilisateur"""
    if request.method == 'POST':
        try:
            user_data = {
                'username': request.form['username'],
                'email': request.form['email'],
                'password': request.form['password'],
                'bio': request.form.get('bio')
            }
            
            user = user_controller.create_user(user_data)
            return jsonify(user), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    
    return render_template('users/register.html')

@user_bp.route('/users/login', methods=['GET', 'POST'])
def login():
    """Connecter un utilisateur"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = user_controller.authenticate_user(email, password)
        if user:
            return jsonify({"message": "Connexion réussie", "user": user}), 200
        else:
            return jsonify({"error": "Identifiants invalides"}), 401
    
    return render_template('users/login.html')