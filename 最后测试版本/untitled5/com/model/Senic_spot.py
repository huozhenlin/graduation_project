# coding:utf8
# from untitled2 import db
from com.factory.app_factory import db

class Senic_spot(db.Model):
    _tablename__ = 'senic_spot_name'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    senic_spot_name =db.Column(db.String(50), nullable=True)
    introduction = db.Column(db.String(255), db.ForeignKey('city.cityname'), nullable=True)
    pic = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    types = db.Column(db.String(4), nullable=True)
    url = db.Column(db.Text, nullable=True)
    levels = db.Column(db.String(20), nullable=True)
    source = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(25), db.ForeignKey('city.cityname'), nullable=True)


    def to_json(self):
        return {
            'id': self.id,
            'senic_spot_name': self.senic_spot_name,
            'introduction': self.introduction,
            'pic': self.pic,
            'price': self.price,
            'types': self.types,
            'url': self.url,
            'levels': self.levels,
            'source': self.source,
            'city': self.city

        }
