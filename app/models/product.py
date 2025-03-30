from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller = db.relationship('User', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f'<Product {self.name}>'

    def get_image_url(self):
        if self.image_path:
            return self.image_path
        return None 