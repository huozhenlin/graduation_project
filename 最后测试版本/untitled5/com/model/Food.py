# coding:utf8
# from untitled2 import db
from com.factory.app_factory import db


class Food(db.Model):
    __tablename__ = 'food'
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    food_name = db.Column(db.String(50))
    food_link = db.Column(db.Text, nullable=True)
    food_pic = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(50),db.ForeignKey('city.cityname'))

    def to_json(self):
        return {
            'id':self.id,
            'food_name':self.food_name ,
            'food_link': self.food_link,
            'food_pic': self.food_pic,
            'city': self.city
        }
