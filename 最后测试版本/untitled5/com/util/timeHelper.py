#coding:utf8
import time,datetime
from time import strftime,gmtime

class timeHelper:
    def __init__(self):
        self.ctime=time.strftime("%Y-%m-%d", time.localtime())
        t = time.strptime(self.ctime, "%Y-%m-%d")
        y, m, d = t[0:3]
        self.curtime = datetime.date(y, m, d)

    def get_curtime(self):
        return strftime("%Y-%m-%d %H:%M:%S", time.localtime())


    def time_helper(self,old_time,new_time):
        a_ = datetime.datetime.strptime(old_time,'%Y-%M-%d')
        b_ = datetime.datetime.strptime(new_time,'%Y-%M-%d')
        c = b_ - a_
        return c.days

    def now_time(self):
        ctime = time.strftime("%Y-%m-%d", time.localtime())
        t = time.strptime(ctime, "%Y-%m-%d")
        y, m, d = t[0:3]
        curtime = str(datetime.date(y, m, d))
        return curtime
