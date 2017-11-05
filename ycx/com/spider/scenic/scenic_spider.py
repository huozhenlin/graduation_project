# coding:utf-8
import requests
import time
from com.util.dbutil import DB
from com.util.constant import HEADER_INFO
from bs4 import BeautifulSoup
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from com.util.timeHelper import timeHelper

'''
景点爬虫类
根据城市表中的城市进行一一爬取
使用request方法爬取，控制速度
目标：http://piao.qunar.com/ticket/list.htm?keyword=%E5%B9%BF%E5%B7%9E&region=&from=mpl_search_suggest
'''
class Scenic:
    def __init__(self,driver):
        self.driver=driver
        self.db=DB()
        self.time=timeHelper()




    #获取城市,包括时间为空或者时间超过当前时间7天的
    def get_city(self):
        city = self.db.select_crawltime()
        for x in city:
            #获取时间

            if x[1] is None:

                url = "http://piao.qunar.com/ticket/list.htm?keyword=%s&region=&from=mpl_search_suggest"%x[0]

                # 爬取完毕，写入时间
                self.db.insert_crawltime(time=self.time.now_time(), city=x[0],colunm_name='scenic_time_crawl')
                # print urlj
                #调用爬虫方法
                self.crawl_pages(to_city=x[0],url=url)
            elif x[1] is not None:
                days = self.time.time_helper(str(x[1]), self.time.now_time())
                print '开始检查时间是否大于七天'
                if days>7:
                    url = "http://piao.qunar.com/ticket/list.htm?keyword=%s&region=&from=mpl_search_suggest" % x[0]

                    # 爬取完毕，写入时间
                    self.db.insert_crawltime(time=self.time.now_time(), city=x[0])
                    # print urlj
                    # 调用爬虫方法
                    self.crawl_pages(to_city=x[0], url=url)




    #爬取指定城市的所有景点
    #包括标题、景区等级、地址、热度、票价、爬取时间、月销售量、来源、简介、图片
    #控制休眠时间
    def crawl_pages(self,to_city,url):

        response = requests.get(url,headers=HEADER_INFO)
        if response.status_code==200:
            #获取到总页数
            content_tree = BeautifulSoup(response.content,'html.parser')
            try:
                pages = content_tree.find('div',id='pager-container').find_all('a')[-2]
                all_pages=pages.text.strip()
                print all_pages
            except Exception as e:
                print '只有一页 '
                all_pages=1
            self.craw_by_pages(to_city=to_city,pages=int(all_pages),url=url)
        else:
            print '错误'





    #根据页数自动爬取
    def craw_by_pages(self,to_city,pages,url):
        #生成url
        for q in range(1,pages+1):
            to_url = url+"&page=%s"%q
            print '开始爬取网址',to_url
            #使用webdriver进行爬取
            self.driver.get(to_url)
            # 将页面滚动条拖到底部
            js = "var q=document.documentElement.scrollTop=100000"
            self.driver.execute_script(js)
            time.sleep(2)
            # response = requests.get(to_url, headers=HEADER_INFO).content
            # 获取到正文
            content_tree = BeautifulSoup(self.driver.page_source, 'html.parser')
            try:
                result_list = content_tree.find('div',class_='result_list').find_all('div',class_='sight_item sight_itempos')
                for item_list in result_list:
                        # 获取img
                        try:
                            img_src = item_list.find('img', class_='img_opacity load')['src']
                        except Exception as e:
                            img_src = 'null'
                            print '找不到图片地址'

                        # 标题
                        try:
                            title = item_list.find('h3', class_='sight_item_caption').text
                        except Exception as e:
                            title='暂无标题'
                            print '找不到标题'
                        # 价格
                        try:
                            price=item_list.find('div',class_='sight_item_pop').text.split()[0][1:]
                            if price.isdigit():
                                price=float(price)
                            else:
                                price=float(0)
                        except Exception as e:
                            print '找不到价格信息'
                            price=float(0)
                        #url
                        try:
                            urls=item_list.find('h3', class_='sight_item_caption').find('a')['href']
                        except Exception as e:
                            urls='null'
                            print '找不到链接'
                        #热度
                        try:
                            hot=item_list.find('span',class_='product_star_level').text.split()[1]
                        except Exception as e:
                            hot='0.0'
                            print '找不到热度'
                        #等级
                        try:
                            level=item_list.find('span',class_='level').text
                        except Exception as e:
                            print '找不到等级信息'
                            level='无等级'
                        #介绍
                        try:
                            intro=item_list.find('div',class_='intro').text
                        except Exception as e:
                            print '找不到介绍'
                            intro='暂无介绍'

                        # 酒店查找
                        num = self.db.if_exist(city_name=to_city, table_name='senic_spot', title=title)
                        if num == 0:
                            self.db.insert_scenic_mess(
                                senic_spot_name=title,
                                introduction=intro,
                                city=to_city,
                                price=price,
                                pic=img_src,
                                types='1000',
                                url='http://piao.qunar.com'+urls,
                                levels=level,
                                hot=hot
                            )
                        else:
                            print '存在'
            except Exception as e:
                print '----错误啦---'
                print e.message
