import os
from flask import Config

class Config(Config):


    # 設定 Flask 和相關套件
    SECRET_KEY = 'A-VERY-LONG-SECRET-KEY'
        
    # RECAPTCHA 公鑰和私鑰
    RECAPTCHA_PUBLIC_KEY = 'A-VERY-LONG-SECRET-KEY'
    RECAPTCHA_PRIVATE_KEY = 'A-VERY-LONG-SECRET-KEY'

    # 資料庫設定，使用環境變數中的值，若無則使用預設值
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    DATABASE_HOST = os.environ.get('DATABASE_HOST')
    DATABASE_PORT = os.environ.get('DATABASE_PORT')
    DATABASE_NAME = os.environ.get('DATABASE_NAME')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

    # Flask-Mail 相關設定
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'gihon12312340@gmail.com'
    MAIL_PASSWORD = 'zrznlnnlxgdclamj'
