import time,datetime
a = '2016-09-18'
b = '2016-09-20'
a_ = datetime.datetime.strptime(a,'%Y-%M-%d')
b_ = datetime.datetime.strptime(b,'%Y-%M-%d')
c = b_ - a_
print c.days