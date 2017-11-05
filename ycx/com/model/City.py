# coding:utf8
from com.factory.app_factory import App_flask
from untitled2 import db

class City(db.Model):
    __tablename__ = 'city'
    cityname = db.Column(db.String(50),primary_key=True)
    introduction = db.Column(db.Text, nullable=True)
    scenic_time_crawl =db.Column(db.Date, nullable=True)
    lat = db.Column(db.String(50), nullable=True)
    lng = db.Column(db.String(50), nullable=True)
    hotel_time_crawl = db.Column(db.Date, nullable=True)
    food_time_crawl = db.Column(db.Date,nullable=True)

    def to_json(self):

        return {
            'cityname':self.cityname ,
            'introduction': self.introduction,
            'scenic_time_crawl': self.scenic_time_crawl,
            'lat': self.lat,
            'lng': self.lng,
            'hotel_time_crawl': self.hotel_time_crawl,
            'food_time_crawl': self.food_time_crawl

        }
