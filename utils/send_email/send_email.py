# -*- coding: utf-8 -*-
import traceback

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header

username = "594154545@qq.com"              #qq账户*
authorization_code = "csoxenvzgwfwbeee"     #qq邮箱授权码*
from_email = "account-email@clonesw.com"            #发送的邮箱


def send_qq_plain_email(from_email, to_emails, title, content):
    """01发送文本邮箱"""
    send_fail = []   #发送出错邮箱列表
    for to_email in to_emails:
        #构建邮箱
        message = MIMEText(content, "plain", "utf-8")        #创建普通邮箱内容使用plain
        message["Subject"] = u"{}--邮箱测试".format(title)             #添加标题
        message["From"] = from_email                                 #添加发件人
        message["To"] = to_email                                    #添加收件人
        try:
            #发送邮件
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)                #创建发送邮箱对象,建立链接
            s.login(username, authorization_code)                   #登录服务器
            s.sendmail(from_email, to_email, message.as_string())   #发送邮箱
            print message.as_string()
            s.quit()                                                #断开链接
            print "发送成功"
        except smtplib.SMTPException, e:
            send_fail.append(to_email)                              #错误邮件添加到列表中
            print "发送失败,%s"%e
    return send_fail


def send_qq_html_email(from_email, to_emails, title, content):
    """02发送html邮箱"""
    send_fail = []
    for to_email in to_emails:
        #构建邮箱
        message = MIMEText(content, "html", "utf-8" )               #创建html邮箱内容使用html
        message["Subject"] = "{}--邮箱验证".format(title)             #标题
        message["From"] = from_email                                #发件人
        message["To"] = to_email                                    #收件人
        try:
            #创建发送邮箱对象
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(username, authorization_code)                   #登录服务器
            s.sendmail(from_email, to_email, message.as_string())   #发送邮箱,支持发送列表
            print message.as_string()
            s.quit()                                                #断开链接
            print "发送成功"
        except smtplib.SMTPException, e:
            send_fail.append(to_email)
            print "发送失败,%s"%e
    return send_fail


def send_qq_attach_email(from_email, to_emails, title, content, attachs):
    """03发送带有附件的邮箱"""
    send_fail = []
    for to_email in to_emails:
        # 创建一个带附件的邮箱对象
        message = MIMEMultipart()  #生成包括多个部分的邮件体
        message.attach(MIMEText(content, "html", "utf-8"))           # 创建html邮箱内容
        message["Subject"] = "{}--邮箱测试".format(title)              #标题
        message["From"] = from_email                                 #发件人
        message["To"] = to_email                                     #收件人
        # 构造附件
        for f in attachs:
            attach = MIMEText(open(f, 'rb').read(), 'base64', 'utf-8')  #创建附件
            attach["Content-Type"] = 'application/octet-stream'         #创建附件请求头
            # filename是邮件中显示的名字
            attach["Content-Disposition"] = 'attachment; filename={}'.format(f)
            message.attach(attach)                                     #附件添加到对象上

        try:
            #创建发送邮箱对象
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(username, authorization_code)
            s.sendmail(from_email, to_email, message.as_string())
            print message.as_string()
            s.quit()
            print "发送成功"
        except smtplib.SMTPException, e:
            send_fail.append(to_email)
            print "发送失败,%s"%e
    return send_fail


def send_qq_img_email(from_email, to_emails, title, content, attachs, imgname):
    """04发送带有图片的html邮箱"""
    send_fail = []
    for to_email in to_emails:
        # 创建一个带附件的实例
        message = MIMEMultipart("related")   #生成包括多个部分的邮件体，采用related定义内嵌资源的邮件体
        message["Subject"] = "{}--邮箱测试".format(title)  #标题
        message["From"] = from_email      #发件人
        message["To"] = to_email      #收件人

        message_alternative = MIMEMultipart('alternative')
        message.attach(message_alternative)
        message_alternative.attach(MIMEText(content, "html", "utf-8"))  # 创建html邮箱内容

        # 打开图片
        image = open(imgname, 'rb')
        msgImage = MIMEImage(image.read())  #创建包含图片数据的邮件体
        image.close()

        # 定义图片id，在html文本中引用
        msgImage.add_header('Content-ID', '<image_test>')
        message.attach(msgImage)


        # 构造附件
        for f in attachs:
            attach = MIMEText(open(f, 'rb').read(), 'base64', 'utf-8')
            attach["Content-Type"] = 'application/octet-stream'
            # filename是邮件中显示的名字
            attach["Content-Disposition"] = 'attachment; filename={}'.format(f)
            message.attach(attach)

        try:
            #创建发送邮箱对象
            print '------sendmail-----'
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(username, authorization_code)
            s.sendmail(from_email, to_email, message.as_string())
            s.quit()
            print "发送成功"
        except smtplib.SMTPException, e:
            send_fail.append(to_email)
            print "发送失败,%s"%e
        except Exception , e:
            print e
    return send_fail
