#coding:utf8

from flask import Flask
from com.util import constant
from flask_sqlalchemy import SQLAlchemy

class App_flask:
    app = Flask('untitled2')
    app.config.from_object(constant)
    db=SQLAlchemy(app)
