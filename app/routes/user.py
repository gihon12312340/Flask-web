from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user
from app import bcrypt, db
from app.email import send_reset_password_mail
from app.forms import RegisterForm, LoginForm, ResetPassworRequestdForm, ResetPasswordForm
from app.models import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
@login_required
def index():
    return render_template('index.html')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email    = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)
        user     = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('註冊成功', category='success')
        return redirect(url_for('user.index'))
    return render_template('user/register.html', form=form)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        
        # 驗證會員帳號密碼是否正確
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash('登入成功', category='info')
            return redirect(url_for('user.index'))
        else:
            flash('登入失敗, 請確認帳號密碼是否正確', category='error')
    return render_template('user/login.html', form=form)

@user_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.login'))

@user_bp.route('/reset_password_reset_request', methods=['GET' ,'POST'])
def send_password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = ResetPassworRequestdForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            token = user.generate_reset_password_token()
            send_reset_password_mail(user, token)
            flash('重置密碼信件已寄出，請確認信箱', category='info')
            return redirect(url_for('user.login'))
        else:
            flash('信箱不存在，請檢查輸入的信箱是否正確', category='error')
    return render_template('user/send_password_reset_request.html', form=form)

@user_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.check_reset_password_token(token)
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('密碼已重置，現在已可以使用新密碼登入', category='info')
            return redirect(url_for('user.login'))
        else:
            flash('重置密碼失敗，請檢查重置密碼的連結是否正確或已過期', category='error')
    return render_template('user/reset_password.html', form=form)