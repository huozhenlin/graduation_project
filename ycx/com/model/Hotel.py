# coding:utf8
from untitled2 import db

class Hotel(db.Model):
    __tablename__ = 'hotel'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hotel_name = db.Column(db.String(25))
    city = db.Column(db.String(255),db.ForeignKey('city.cityname'), nullable=True)
    pic = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    types = db.Column(db.String(4), nullable=True)
    url = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(100),nullable=True)
    source = db.Column(db.String(20),nullable=True)

    def to_json(self):
        return {
            'hotel_name':self.hotel_name ,
            'city': self.city,
            'pic': self.pic,
            'price': self.price,
            'types': self.types,
            'url': self.url,
            'address': self.address,
            'source':self.source

        }
