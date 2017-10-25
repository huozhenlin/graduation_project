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
        sql = "select cityname,time_crawl from city"
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
    def insert_crawltime(self,time,city):
        try:
            sql02="update city set time_crawl='%s'where cityname='%s'"%(time,city)
            print sql02
            self.cursor.execute(sql02)
            self.conn.commit()
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


# DB().insert_scenic_mess(
#     senic_spot_name='桃山公园',
#     introduction='远远望去，郁郁葱葱，繁花似锦，莺歌燕舞',
#     price=0,
#     city='七台河市',
#     url='http://piao.qunar.com/ticket/detail_1487394487.html?st=a3clM0QlRTQlQjglODMlRTUlOEYlQjAlRTYlQjIlQjMlRTUlQjglODIlMjZpZCUzRDE5MDY4NyUyNnR5cGUlM0QwJTI2aWR4JTNEMSUyNnF0JTNEcmVnaW9uJTI2YXBrJTNEMiUyNnNjJTNEV1dXJTI2YWJ0cmFjZSUzRGJ3ZCU0MCVFNSVBNCU5NiVFNSU5QyVCMCUyNmxyJTNEJUU2JUI3JUIxJUU1JTlDJUIzJTI2ZnQlM0QlN0IlN0Q%3D#from=mpl_search_suggest',
#     pic='http://img1.qunarzz.com/sight/p0/201403/11/8d20a44b58e581574c8d5c52dafe054d.jpg_280x200_16b2f8f7.jpg',
#     types='1000',
#     hot='0.0',
#     levels='无等级'
# )