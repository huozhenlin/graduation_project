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