#coding:utf-8
"""
@file:      emailClass.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    2.7
@editor:    PyCharm
@create:    2016-8-12 14:30
@description:
            smtp发送邮件，对email类做一个简单的封装,
            注意python3.3以上smtp.starttls()会报错
"""

import smtplib
from email.mime.text import MIMEText  
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import platform

class Email:
    def __init__(
            self,sender,receiver,subject,content,
            subtype='plain',img_src=None
    ):
        if float(platform.python_version()[:3])>3.4:
            raise ImportError('Email Class():Please use python version under 3.4')
        self.msg = MIMEMultipart('mixed')
        msgText = MIMEText(content,_subtype=subtype,_charset='utf-8')
        self.msg.attach(msgText)
        if img_src:
            fp = open(img_src,'rb')
            msgImage = MIMEImage(fp.read())
            msgImage.add_header('Content-ID','<meinv_image.png>')
            self.msg.attach(msgImage)
            fp.close()
        self.msg['Subject'] = Header(subject, 'utf-8')
        self.msg['From'] = sender
        self.msg['To'] = receiver
        self.sender = sender
        self.receiver = receiver
        self.smtp = smtplib.SMTP()


    def conn_server(self,host,port):
        #连接服务器,并启动tls服务
        try:
            self.smtp.connect(host,port)
            self.smtp.starttls()
        except Exception as e:
            print('conn_server():',e)


    def login(self,username,password):
        try:
            self.smtp.login(username, password)
            log_string = username+'登陆成功'+'\n'
            print(log_string)#可以考虑写在日志里
        except Exception as e:
            print('login():',e)


    def send(self):
        try:
            self.smtp.sendmail(self.sender, self.receiver, self.msg.as_string())
            log_string = '邮件已投至'+self.receiver+'\n'
            print(log_string)
        except Exception as e:
            print('send():',e)


    def close(self):
        self.smtp.close()



def remind_me(admin_address):
    emailAI = Email(
        receiver = admin_address,
        sender   = 'luyangaini@vip.qq.com',
        subject  = '爬虫一小时没采到信息了，上线看看吧',
        content  = 'rt',
    )
    emailAI.conn_server(
        host='smtp.qq.com',
        port = 587
    )
    emailAI.login(
        username='luyangaini@vip.qq.com',
        password='ptuevbbulatcbcfh'
    )
    emailAI.send()
    emailAI.close()


if __name__=='__main__':
    map(remind_me,['965606089@qq.com','gaotongfei1995@gmail.com'])
