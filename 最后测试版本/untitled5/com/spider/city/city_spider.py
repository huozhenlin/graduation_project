#coding:utf8
import requests,time,re,json
from bs4 import BeautifulSoup
from com.util.constant import HEADER_INFO,BAIDUMAP_AK
from com.util.dbutil import DB

# 定义一个城市类，实现城市经纬度，介绍的爬取
from com.util.mailHelper import sendMail


class City:
    def __init__(self):
        self.headers=HEADER_INFO
        self.db=DB()
    # 获取城市百度百度可经纬度介绍
    def get_city_intro(self):

        city_list=self.db.select_cityname()
        for x in city_list:
            url='https://baike.baidu.com/item/'+x[0]
            try:
                content=requests.get(url,headers=self.headers)
                print content.status_code
                html_contents=BeautifulSoup(content.content,'html.parser')
                content = html_contents.find('div',class_='lemma-summary').text
                print content
                self.db.insert_city_intro(city=x[0],intro=content)
                time.sleep(0.5)
            except Exception as e:
                sendMail('城市爬虫出错啦，请注意')
                print e.message

    #获取城市经纬度
    def get_city_lat_lng(self):
        city_list=self.db.select_city_loc()

        for x in city_list:
            city_name=x[0]
            url = "http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=%s&callback=showLocation" %(city_name,BAIDUMAP_AK)
            print url
            # 更新之前先对表检查，确保经纬为为空的行才被更改
            location = self.getlal(url)
            print location
            self.db.insert_city_loc(location=location,city=x[0])

     #通过城市名获取经纬度
    def getlal(self, lal):
        try:
            time.sleep(0.02)
            res = requests.get(url=lal)
            # {"status":0,"result":{"location":{"lng":114.0259736573215,"lat":22.546053546205248},"precise":0,"confidence":14,"level":"城市"}}
            json_data = res.text
            value_lal = re.findall(r'\([\s\S]*\)', json_data)[0][1:-1]
            jd = json.loads(value_lal)
            # 得到纬度
            lat = jd['result']['location']['lat']
            # print lat
            # 得到纬度
            lng = jd['result']['location']['lng']
            # print lng
            return [lat, lng]
        except Exception as e:
            print e.args
            print '网络错误'
