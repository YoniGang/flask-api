from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__) 
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Set logging file
handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)
log.addHandler(handler)

from flask_message_app.routes import messages
from flask_message_app.routes import users

    