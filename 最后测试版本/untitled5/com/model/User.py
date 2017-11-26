# coding:utf8
from com.factory.app_factory import db
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(13), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self,*args,**kwargs):
        account=kwargs.get('account')
        password=kwargs.get('password')

        self.account=account
        self.password=generate_password_hash(password)


    def check_pass(self,raw_password):
        result=check_password_hash(self.password,raw_password)
        return result