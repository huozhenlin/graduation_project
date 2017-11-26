#!/usr/bin/env python3
# coding: utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from com.util import constant
sender = constant.msg_from  #发件人
receiver = constant.msg_to  #收件人
subject = '毕业设计爬虫'  #主题
smtpserver = constant.smtpserver   #服务器
username = constant.msg_from   #用户名
password = constant.passwd  #密码

def sendMail(text):
    print (type(text))
    msg = MIMEText(text, 'plain', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
    msg['Subject'] = Header(subject, 'utf-8')

    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        print ('success')
    except smtplib.SMTPException as e:
        print (e.args)
        print ('fail')
    finally:
        smtp.quit()