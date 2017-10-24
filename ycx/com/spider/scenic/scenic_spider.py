# coding:utf-8
import bs4
from bs4 import BeautifulSoup
import urllib
import xlwt
import time
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def crawl(html_string):
    #    respons = urllib.urlopen(url)
    #    soup    = BeautifulSoup(respons.read())
    soup = BeautifulSoup(html_string)
    name = ""
    level = ""
    address = ""
    money = ""
    # 分析网页提取信息，这一部分需要熟悉beautifulsoup
    for tag in soup.find_all(["span"]):  # 利用beautifulsoup提取所有span标签
        if "class" in tag.attrs:
            if "mp-description-name" in tag.attrs["class"]:  # 如果其class包含name,那么就是景区名称，下面同理
                name = str(tag.string)
            if "mp-description-level" in tag.attrs["class"]:
                level = str(tag.string)
            if "mp-description-address" in tag.attrs["class"]:
                address = str(tag.string)
        else:
            for j in tag.children:  # 提取票价时，在span的子标签span中
                if type(j) == bs4.element.Tag and j.name == "span":
                    money = str(j.string)
    information = (address, name, level, money)
    return information


# ======python读入excel表初始化
book = xlwt.Workbook(encoding="utf-8", style_compression=0)
sheet = book.add_sheet("where_we_go", cell_overwrite_ok=True)
sheet.write(0, 0, "景区地址")  # 第一行为四个属性名字，整个表为n行×4列，n为抓取到的景区个数
sheet.write(0, 1, "景区名称")
sheet.write(0, 2, "景区级别")
sheet.write(0, 3, "景区票面价")

start_time = time.time()
line_num = 1
for i in xrange(0, 1000):  # 2500000000，最大2295597022   #有相当多的景区，这一点吓尿，n大的时候必须用xrange，用range生成一个列表太大崩溃。
    url = "http://piao.qunar.com/ticket/detail_" + str(i) + ".html"
    respons = urllib.urlopen(url)
    if respons.geturl() != url:  # 抓取太快又会发生重定向的问题，重定向后的url网页显示“尊敬的用户，安全系统检测到异常访问，当前请求已经被拦截”
        print respons.geturl()
    html_string = respons.read()
    if "mp-description-detail" in html_string:  # 判断是否有这个网页，像是标号为0的，就没有，1为齐庐山，2为中国竹艺城等等，
        information = crawl(html_string)  # 进行抓取任务，返回四个主要属性值
        for j in range(len(information)):
            sheet.write(line_num, j, information[j])  # 写入excel表中。
        line_num += 1
        print "处理url:", i, information[1]
    if line_num % 10 == 0:
        end_time = time.time()
        print "time:", end_time - start_time
    else:
        continue

book.save("where.xls")  # 要吧excel进行保存