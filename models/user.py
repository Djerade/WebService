from ..database import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary for easier handling"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
        }
    
    @classmethod
    def get_all(cls):
        """Retrieve all users"""
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, user_id):
        """Retrieve a user by ID"""
        return cls.query.get(user_id)
    
    @classmethod
    def create(cls, username, email):
        """Create a new user"""
        new_user = cls(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    def update(self, username=None, email=None):
        """Update user details"""
        if username:
            self.username = username
        if email:
            self.email = email
        db.session.commit()
        return self
    
    def delete(self):
        """Delete the user"""
        db.session.delete(self)
        db.session.commit()