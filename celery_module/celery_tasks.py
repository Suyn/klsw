# -*- coding: utf-8 -*-
from __future__ import absolute_import
from utils.send_email.send_email import send_qq_html_email
import time
import redis, json
from celery_module.celery import celery_test
conn = redis.Redis()


# @celery_test.task
# def add(a, b):
#     time.sleep(2)
#     return a+b

@celery_test.task
def manage_redis():
    regist_email_list = conn.keys("*regist_email:*")
    print regist_email_list
    if regist_email_list:
        for i in regist_email_list:
            org_regist_data = conn.get(i)
            print org_regist_data
            regist_data = json.loads(org_regist_data)
            if regist_data['IsSendEmail'] == 'no':
                e_mail_list = []
                email = regist_data['email']
                username = regist_data['username']
                password = regist_data['password']
                code_time = regist_data['code_time']
                e_mail_list.append(email)
                content = u"""
                您好，<a href="http://clonesw.com">克隆生物</a>提醒您，您正在进行注册操作,
                请<a href="http://clonesw.com/email_confirm?email={}&username={}&password={}&code_time={}">点击该链接进行绑定</a>，
                有效时间为30分钟，若非您本人所为请忽略此邮件。
                """.format(email, username, password, code_time)
                send_qq_html_email("account-email@clonesw.com", e_mail_list, "注册", content)
                modify_regist_data = org_regist_data.replace('no', 'yes')
                conn.setex('regist_email:%s' % regist_data['email'], modify_regist_data, 1800)
