from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange

from app.models import User, ProductsList

class RegisterForm(FlaskForm):

    username  = StringField('帳號', validators=[DataRequired(), Length(min=6, max=20)])
    email     = StringField('信箱', validators=[DataRequired(), Email()])
    password  = PasswordField('密碼', validators=[DataRequired(), Length(min=8, max=20)])
    confirm   = PasswordField('再輸入一次密碼', validators=[DataRequired(), EqualTo('password')])
    submit    = SubmitField('註冊')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('帳號已被使用')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('信箱已被使用')
        
class LoginForm(FlaskForm):

    username  = StringField('帳號', validators=[DataRequired(), Length(min=6, max=20)])
    password  = PasswordField('密碼', validators=[DataRequired(), Length(min=8, max=20)])
    remember  = BooleanField('記住我')
    submit    = SubmitField('登入')

class ResetPassworRequestdForm(FlaskForm):

    email     = StringField('信箱', validators=[DataRequired(), Email()])
    submit    = SubmitField('寄出')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
                raise ValidationError('信箱不存在')
            
class ResetPasswordForm(FlaskForm):

    password  = PasswordField('新密碼', validators=[DataRequired(), Length(min=8, max=20)])
    confirm   = PasswordField('再輸入一次密碼', validators=[DataRequired(), EqualTo('password')])
    submit    = SubmitField('重置密碼')

class EditProductsForm(FlaskForm):

    product_name  = StringField('商品名稱', validators=[DataRequired()])
    product_price = StringField('商品價格', validators=[DataRequired()])
    submit_add    = SubmitField('新增商品')
    submit_remove = SubmitField('移除商品')

    def validate_product_name(self, product_name):
        if self.submit_add.data:
            existing_product = ProductsList.query.filter_by(product_name=product_name.data).first()
            if existing_product:
                raise ValidationError('商品已經存在')
            
class OrderForm(FlaskForm):

    order_quantities = IntegerField('數量', validators=[DataRequired(), NumberRange(min=0)], default=0)
    submit_oder      = SubmitField('加入購物車')
