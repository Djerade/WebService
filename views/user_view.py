from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..controllers.user_controller import UserController

user_bp = Blueprint('users', __name__)

@user_bp.route('/users')
def list_users():
    """View to list all users"""
    users = UserController.list_users()
    return render_template('users/list.html', users=users)

@user_bp.route('/users/create', methods=['GET', 'POST'])
def create_user():
    """View to create a new user"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        try:
            UserController.create_user(username, email)
            flash('User created successfully!', 'success')
            return redirect(url_for('users.list_users'))
        except Exception as e:
            flash(f'Error creating user: {str(e)}', 'error')
    return render_template('users/create.html')

@user_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    """View to edit an existing user"""
    user = UserController.get_user(user_id)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        try:
            UserController.update_user(user_id, username, email)
            flash('User updated successfully!', 'success')
            return redirect(url_for('users.list_users'))
        except Exception as e:
            flash(f'Error updating user: {str(e)}', 'error')
    return render_template('users/edit.html', user=user)

@user_bp.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """View to delete a user"""
    try:
        UserController.delete_user(user_id)
        flash('User deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting user: {str(e)}', 'error')
    return redirect(url_for('users.list_users'))