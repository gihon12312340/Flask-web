import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_CONFIG'))
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
login.login_view = 'user.login'  
login.login_message = 'You must to access this page'
login.login_message_category = 'info'
mail = Mail(app)

from app.routes.user import user_bp
from app.routes.products import products_bp
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(products_bp, url_prefix='/products')

def create_db_if_not_exists():
    with app.app_context():
        db.create_all()

if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_db_if_not_exists()
