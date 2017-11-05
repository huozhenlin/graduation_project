# coding:utf8
from untitled2 import db
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(13), nullable=False)
    password = db.Column(db.String(50), nullable=False)
