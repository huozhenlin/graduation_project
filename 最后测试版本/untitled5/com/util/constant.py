#coding:utf8
#浏览器头信息

import os
HEADER_INFO = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
}
#百度地图开发者秘钥
BAIDUMAP_AK ="t3vn5Rb35MhGsqv1recs9Qojbwz7Kiqb"

#数据库
DATABASE='ycx'

#数据库账号
DB_ACCOUNT ='root'

#数据库密码
DB_PASSWORD = '1234'

# 发送方邮箱
msg_from = '13580044203@139.com'

# 填入发送方邮箱的授权码
passwd = 'huo131415'

# 收件人邮箱
msg_to = '1031734796@qq.com'

#服务器
smtpserver = 'smtp.139.com'

DEBUG=True

SECRET_KEY=os.urandom(24)

HOSTNAME='127.0.0.1'

PORT='3306'

URL='/ycx/'

DB_URI='mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(
    DB_ACCOUNT,DB_PASSWORD,HOSTNAME,PORT,DATABASE
)

SQLALCHEMY_DATABASE_URI=DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS=False
