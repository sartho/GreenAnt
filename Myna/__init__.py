from flask import Flask
from Myna.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os

from flask_mongoengine import MongoEngine

Myna = Flask(__name__)
Myna.config.from_object(Config)

db = SQLAlchemy(Myna)
migrate = Migrate(Myna, db)

login = LoginManager(Myna)
login.login_view = 'login'

photos = UploadSet('photos', IMAGES)
configure_uploads(Myna, photos)
patch_request_class(Myna)  # set maximum file size, default is 16MB

md = MongoEngine()

from Myna.GreenAnt import gn as Green_Ant
Myna.register_blueprint(Green_Ant,url_prefix='/Green_Ant')

from Myna import routes

if not Myna.debug:
    if Myna.config['MAIL_SERVER']:
        auth = None
        if Myna.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (Myna.config['MAIL_USERNAME'], Myna.config['MAIL_PASSWORD'])
        secure = None
        if Myna.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(Myna.config['MAIL_SERVER'], Myna.config['MAIL_PORT']),
            fromaddr='no-reply@' + Myna.config['MAIL_SERVER'],
            toaddrs=Myna.config['ADMINS'], subject='Myna APP Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        Myna.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/Myna.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    Myna.logger.addHandler(file_handler)

    Myna.logger.setLevel(logging.INFO)
    Myna.logger.info('Myna startup')