#coding:utf8
import requests
import time
from com.util.dbutil import DB
from bs4 import BeautifulSoup
from selenium import webdriver
import sys
from xpinyin import Pinyin
import re
from com.util.timeHelper import timeHelper
reload(sys)
sys.setdefaultencoding('utf-8')


'''
酒店爬虫类，爬取艺龙网数据
url:http://hotel.elong.com/beijing/
'''

class Hotel:
    def __init__(self,driver):
        self.db=DB()
        self.pinyin=Pinyin()
        self.driver=driver
        self.time = timeHelper()

    #获取到城市
    def get_city(self):
        city = self.db.select_crawltime()
        for x in city:
            # 获取时间
            if x[2] is None:
                # 爬取完毕，写入时间
                self.db.insert_crawltime(time=self.time.now_time(), city=x[0], colunm_name='hotel_time_crawl')
                self.to_pinyin(x[0])
            elif x[2] is not None:
                days = self.time.time_helper(str(x[2]), self.time.now_time())
                print '天数是',days
                print '开始检查时间是否大于七天'
                if days > 7:
                    # 爬取完毕，写入时间
                    self.db.insert_crawltime(time=self.time.now_time(), city=x[0], colunm_name='hotel_time_crawl')
                    self.to_pinyin(x[0])
            else:
                print '不进行搜索'




    def to_pinyin(self,city):
        cityname = city.replace('市', '')
        pinyins = self.pinyin.get_pinyin(cityname, '')
        # 组装url
        to_url = 'http://hotel.elong.com/%s/' % pinyins
        # 调用爬取的方法
        print '开始爬取网站', to_url
        try:
            self.crawl_hotel(url=to_url, city_name=city)
        except Exception as e:
            print '超时'

    #爬取内容
    def crawl_hotel(self,url,city_name):
        self.driver.get(url)
        # 将页面滚动条拖到底部
        js = "var q=document.documentElement.scrollTop=100000"
        self.driver.execute_script(js)
        time.sleep(2)
        #捉取页数
        try:
            a_tag=BeautifulSoup(self.driver.page_source,'html.parser').find('div',id='pageContainer')
            page=a_tag.find_all('a')[-2].text
        except Exception as e:
            page=0

        #如何page是1页
        if page!=0:
            #先获取页面内容，再刷新页面
            page=int(page)+1
            print '共有页数为',page
            for x in xrange(1,page):
                print x
                try:
                    if x==1:
                        content=BeautifulSoup(self.driver.page_source,'html.parser').find('div',id='hotelContainer')
                        hotel_list=content.find_all('div',class_='h_item')
                        for hl in hotel_list:
                            self.analyse_html(hl=hl,city=city_name)
                    else:
                        self.driver.find_element_by_class_name('page_next').click()
                        time.sleep(10)
                        # 将页面滚动条拖到底部
                        js = "var q=document.documentElement.scrollTop=100000"
                        self.driver.execute_script(js)
                        content = BeautifulSoup(self.driver.page_source, 'html.parser').find('div', id='hotelContainer')
                        hotel_list = content.find_all('div', class_='h_item')
                        for h2 in hotel_list:
                            self.analyse_html(hl=h2,city=city_name)

                except Exception as e:
                    print e.message
                    print '无内容'


    def analyse_html(self,hl,city):
        # 酒店名
        try:
            hotel_name = hl.find('p', class_='h_info_b1').text.strip()
            to_hotel_name = re.sub('\d*', '', hotel_name)

            # 价格
            try:
                hotel_price = hl.find('span', class_='h_pri_num').text.strip()
                hotel_price = float(hotel_price)
            except Exception as e:
                hotel_price = float(0)
                print '找不到酒店价格'

            # 位置
            try:
                hotel_address = hl.find('p', class_='h_info_b2').text.strip()
            except Exception as e:
                hotel_address = '未发现'
                print '找不到酒店地址'

            # 图片
            try:
                hotel_img = hl.find('div', class_='h_info_pic').find_all('img')[0]['src']
            except Exception as e:
                print '找不到图片'

            # url
            try:
                hotel_link = hl.find('p', class_='h_info_b1').find('a')['href']
            except Exception as e:
                print '找不大链接'

            #酒店查找
            num=self.db.if_exist(city_name=city,table_name='hotel',title=hotel_name)
            if num==0:
                self.db.insert_hotel_mess(hotel_name=to_hotel_name,
                                          hotel_address=hotel_address,
                                          hotel_price=hotel_price,
                                          hotel_link=hotel_link,
                                          hotel_pic='http://hotel.elong.com'+hotel_img,
                                          city=city,
                                          source='艺龙网'

                                          )
            else:
                print '存在'


        except Exception as e:
            print e.message
            print '找不到酒店名,跳过'


