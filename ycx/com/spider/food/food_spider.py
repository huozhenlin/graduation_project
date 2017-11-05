# coding:utf8
from bs4 import BeautifulSoup
from selenium import webdriver
import re, time
from com.util.dbutil import DB
from com.util.timeHelper import timeHelper
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

'''
美食爬虫类，爬取城市特色美食
URL:http://home.meishichina.com/search/recipe/%E5%8C%97%E4%BA%AC/?
'''


class Food:
    def __init__(self, driver):
        self.driver = driver
        self.db = DB()
        self.time = timeHelper()

    # 提取城市
    def get_city(self):
        city = self.db.select_crawltime()
        for x in city:
            # 获取时间
            if x[3] is None:
                # 爬取完毕，写入时间
                self.db.insert_crawltime(time=self.time.now_time(), city=x[0], colunm_name='food_time_crawl')
                cityname = x[0].replace('市', '')
                self.crawl_food(cityname)
            elif x[3] is not None:
                days = self.time.time_helper(str(x[3]), self.time.now_time())
                print '天数是', days
                print '开始检查时间是否大于七天'
                if days > 7:
                    # 爬取完毕，写入时间
                    self.db.insert_crawltime(time=self.time.now_time(), city=x[0], colunm_name='food_time_crawl')
                    cityname = x[0].replace('市', '')
                    self.crawl_food(cityname)
            else:
                print '不进行搜索'

    # 爬取数据,
    # 接收城市参数
    # 需要爬取图片，名字
    def crawl_food(self, city):
        url = 'http://home.meishichina.com/search/recipe/%s/?' % (city)
        self.driver.get(url)
        # 将页面滚动条拖到底部
        js = "var q=document.documentElement.scrollTop=100000"
        self.driver.execute_script(js)
        page_content = BeautifulSoup(self.driver.page_source, 'html.parser')

        try:
            all_pages = page_content.find('div', class_='ui_title_wrap').find('span').text
            #结果数
            all_page = re.findall(r'\d+', all_pages)[0]
            print all_page

            if int(round(float(all_page) / 20))+1 ==1:
                self.analyse_html(page_content=page_content, city=city)
            # 根据不同条件点击下一页
            else:
                try:
                    for p in xrange(1, int(round(float(all_page) / 20))+1):
                        if p == 1:
                            self.analyse_html(page_content=page_content, city=city)
                        else:
                            # 找到下一页按钮点击
                            self.driver.find_element_by_link_text('下一页').click()
                            time.sleep(10)
                            # 将页面滚动条拖到底部
                            js = "var q=document.documentElement.scrollTop=100000"
                            self.driver.execute_script(js)
                            page_content01 = BeautifulSoup(self.driver.page_source, 'html.parser')
                            self.analyse_html(page_content=page_content01, city=city)
                            time.sleep(5)
                except Exception as e:
                    print e.message
        except Exception as e:
            print '找不到页数'

    def analyse_html(self, page_content, city):
        try:
            content_list = page_content.find('div', id='search_res_list').find_all('li')
            for x in content_list:
                food_link = x.find('div', class_='pic').find('a')['href']
                food_pic = x.find('div', class_='pic').find('img')['src']
                food_name = x.find('div', class_='detail').find('h4').text
                data=self.db.if_exist(city_name=city+'市',table_name='food',title=food_name)
                print data
                if data==0:
                    self.db.insert_food_mess(city=city + '市', food_link=food_link, food_pic=food_pic, food_name=food_name)
                else:
                    print '存在'
        except Exception as e:
            print e.message
            print '网页具体内容找不到'

