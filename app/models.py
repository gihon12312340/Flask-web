from app import db, login
from flask_login import UserMixin
from flask import current_app
import jwt

@login.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
    def generate_reset_password_token(self):
        return jwt.encode({'id': self.id}, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def check_reset_password_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.query.filter_by(id=data['id']).first()
        except jwt.ExpiredSignatureError:
            return None  # Token過期
        except jwt.InvalidTokenError:
            return None  # 無效的Token
        
class ProductsList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name  = db.Column(db.String(20), unique=True, nullable=False)
    product_price = db.Column(db.String(20), nullable=False)


class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name  = db.Column(db.String(20), nullable=False)
    product_price = db.Column(db.Integer, nullable=False)
    quantity      = db.Column(db.Integer, nullable=False) 
    user_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='shoppingcart', lazy=True)
    
class OrderList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total         = db.Column(db.Integer, nullable=False)
    completed     = db.Column(db.Boolean, default=False)
    user_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user        = db.relationship('User', backref='orderslist', lazy=True)
    order_items = db.relationship('OrderItem', backref='orderlist', lazy=True)

    
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name  = db.Column(db.String(100), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    quantity      = db.Column(db.Integer, nullable=False)
    total         = db.Column(db.Float, nullable=False)
    order_id      = db.Column(db.Integer, db.ForeignKey('order_list.id'), nullable=False)