from ..models.user import User

class UserController:
    @staticmethod
    def list_users():
        """Retrieve all users"""
        return User.get_all()
    
    @staticmethod
    def get_user(user_id):
        """Get a specific user"""
        return User.get_by_id(user_id)
    
    @staticmethod
    def create_user(username, email):
        """Create a new user"""
        return User.create(username, email)
    
    @staticmethod
    def update_user(user_id, username=None, email=None):
        """Update an existing user"""
        user = User.get_by_id(user_id)
        if user:
            return user.update(username, email)
        return None
    
    @staticmethod
    def delete_user(user_id):
        """Delete a user"""
        user = User.get_by_id(user_id)
        if user:
            user.delete()
            return True
        return False