#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import smtplib
from email.mime.text import MIMEText
from email.header import Header
 
# 第三方 SMTP 服务
mail_host="smtp.qq.com"  #设置服务器
mail_user="454201948@qq.com"    #用户名
mail_pass="xwiifttktijubibi"   #口令 
 
 
# 自己给自己发邮件
sender = '454201948@qq.com'
receivers = ['494244808@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("菜鸟教程", 'utf-8')
message['To'] =  Header("测试", 'utf-8')
 
smtpObj = smtplib.SMTP() 
smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
smtpObj.login(mail_user,mail_pass)
subject=None
 
def sendEmail(newStock):
    global smtpObj,message
    try:
        subject = '您好，您有新的财富'
        for i in newStock:
            subject += i
        message['Subject'] = Header(subject, 'utf-8')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

if __name__ == '__main__':
    sendEmail(['123456'])
    