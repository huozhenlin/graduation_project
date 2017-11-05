# coding:utf8
import sys
from selenium import webdriver
from untitled2 import db,Task

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class Spider_task:


    def taks(self, id):
        # 获取爬虫配置信息
        args = id
        result = Task.query.filter_by(id=args).first()
        print '----------------线程爬虫已经启动-------------------'
        print result.spider_type
        if result:
            type = ["旅游景点", "酒店", "特色美食"]
            types = list(result.spider_type.split(","))
            for x in types:
                if type[int(x)] == "旅游景点":
                    print '开始爬取旅游景点信息'
                    from com.spider.food.food_spider import Food
                    Food(webdriver.Chrome()).get_city()
                elif type[int(x)] == "酒店":
                    print '开始爬取酒店信息'
                    from com.spider.hotel.hotel_spider import Hotel
                    Hotel(webdriver.Chrome()).get_city()
                elif type[int(x)] == "特色美食":
                    print '开始爬取特色美食信息'
                    from com.spider.scenic.scenic_spider import Scenic
                    Scenic(driver=webdriver.Chrome()).get_city()
            result.status = 1
            db.session.commit()
        else:
            pass
