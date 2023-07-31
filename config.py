import os
from flask import Config

class Config(Config):

    #SECRET KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A-VERY-LONG-SECRET-KEY'
    
    #RECAPTCHA PUBLIC KEY
    RECAPTCHA_PUBLIC_KEY  = os.environ.get('RECAPTCHA_PUBLIC_KEY') or 'A-VERY-LONG-SECRET-KEY'
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or 'A-VERY-LONG-SECRET-KEY'

    
    #Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 設定 Flask-Mail 相關設定
    MAIL_SERVER   = os.environ.get('MAIL_SERVER')
    MAIL_PORT     = 587
    MAIL_USE_TLS  = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or'example@gmail.com'  
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or'0000'

