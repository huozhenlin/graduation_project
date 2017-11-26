#coding:utf8
import pandas as pd
import MySQLdb
from com.util.constant import DB_ACCOUNT,DB_PASSWORD,DATABASE
# 定义一个数据库操作类
class DB:
    # 构造函数
    def __init__(self):
        self.conn = MySQLdb.connect(
            host="localhost",
            user=DB_ACCOUNT,
            passwd=DB_PASSWORD,
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        self.conn.select_db(DATABASE)

    # 插入城市名
    def insert_cityname(self):
        city = pd.read_csv('C:\Users\hzl\Desktop\city.csv')
        city_column = city['city']
        for x in city_column:
            sql = "insert into city set cityname='%s'"%x
            print sql
            self.cursor.execute(sql)

        self.conn.commit()

    # 写入城市介绍,参数分别为城市名、介绍
    def insert_city_intro(self,city,intro):
        try:
            sql = "update  city set introduction ='%s' where cityname='%s'"%(intro,city)
            print sql
            self.cursor.execute(sql)
            self.conn.commit()

        except Exception as e:
            print '数据库插入异常'
            self.conn.rollback()

    # 查询城市名,减少查询次数
    def select_cityname(self):
        sql = "select cityname from city where introduction is NULL "
        print sql
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    # 查询城市名，时间
    def select_crawltime(self):
        sql = "select cityname,scenic_time_crawl,hotel_time_crawl,food_time_crawl from city"
        print sql
        self.cursor.execute(sql)
        data =  self.cursor.fetchall()
        return data

    # 查询城市经纬度为空的所有城市
    def select_city_loc(self):
        try:
            sql01="select cityname from city where lng is NULL"
            self.cursor.execute(sql01)
            data=self.cursor.fetchall()
            return data
        except Exception as e:
            print e.message
        # sql02="update city set location='%s' WHERE cityname='%s'"

    # 写入查询时间
    def insert_crawltime(self,time,city,colunm_name):
        try:
            sql02="update city set %s='%s'where cityname='%s'"%(colunm_name,time,city)
            print sql02
            self.cursor.execute(sql02)
            self.conn.commit()
        except Exception as e:
            print e.message
            self.conn.rollback()

    # 根据城市查询酒店或者美食或者景点是否存在
    def if_exist(self,city_name,table_name,title):
        try:
            if table_name =='scenic_spot':
                sql03 = "select count(*) from %s where senic_spot_name='%s' and city ='%s'"%(table_name,title,city_name)
            elif table_name =='hotel':
                sql03 = "select count(*) from %s where hotel_name='%s' and city ='%s'"%(table_name,title,city_name)
            else:
                sql03 = "select count(*) from %s where food_name='%s' and city ='%s'"%(table_name,title,city_name)

            print sql03
            self.cursor.execute(sql03)
            data = self.cursor.fetchall()
            return data[0][0]
        except Exception as e:
            print e.message
            self.conn.rollback()

    # 更新城市经纬度为空的所有城市
    def insert_city_loc(self,location,city):
        try:
            sql = "update city set lng='%s',lat='%s' where cityname='%s'" % (
                location[1], location[0], city)
            print sql
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print e.args
            self.conn.rollback()

    # 将景点信息存入数据库
    def insert_scenic_mess(self,senic_spot_name,introduction,price,city,pic,types,url,hot,levels):
        try:

            print '图片地址', pic
            print '标题', senic_spot_name
            print '价格', price
            print '链接', url
            print '热度', hot
            print '等级', levels
            print '介绍', introduction
            print '类型',types
            print '城市',city
            # sql="insert into senic_spot(senic_spot_name,introduction,city,pic,price,types,url,hot,levels)VALUES " \
            #     "('%s','%s','%s','%s',%d,'%s','%s','%s','%s')"%(senic_spot_name,introduction,city,pic,price,types,url,hot,level)
            sql="insert into senic_spot(senic_spot_name,introduction,city,pic,price,types,url,hot)VALUES " \
                "('%s','%s','%s','%s',%f,'%s','%s','%s')"%(senic_spot_name,introduction,city,pic,price,types,url,hot)
            print sql
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print '插入错误'
            print e.message
            self.conn.rollback()

    # 将美食信息存入数据库
    def insert_food_mess(self,city,food_pic,food_name,food_link):
            try:
                sql = "insert into food(food_name,food_link,city,food_pic)VALUES " \
                      "('%s','%s','%s','%s')" % (
                      food_name,food_link,city,food_pic)
                print sql
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print '插入错误'
                print e.message
                self.conn.rollback()


    # 将旅店信息插入数据库
    def insert_hotel_mess(self,hotel_name,hotel_address,hotel_price,hotel_pic,hotel_link,city,source):
        try:


            print '酒店名是', hotel_name
            print '酒店价格是', hotel_price
            print '酒店地址是', hotel_address
            print '酒店图片是', hotel_pic
            print '酒店链接是', hotel_link
            print '城市是',city

            sql="insert into hotel(hotel_name,city,pic,price,types,url,address,source)VALUES " \
                "('%s','%s','%s',%f,'%s','%s','%s','%s')"%(hotel_name,city,hotel_pic,hotel_price,'1002',hotel_link,hotel_address,source)
            print sql
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print '插入错误'
            print e.message
            self.conn.rollback()
