from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
# from logging.handlers import RotatingFileHandler

app = Flask(__name__) 
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from flask_message_app import routes

    