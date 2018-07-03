# -*- coding: utf-8 -*-
import time

from handlers.BaseHandler.base import BaseHandler
from module.account.user_account import User
from libs.account.account_lib import personal_login_lib, login_lib, forget_lib, regist_email_lib


class LoginHandler(BaseHandler):
    """用户登录"""
    def get(self):
        return self.render('account/sign-in.html')

    def post(self):
        account_user = self.get_argument('account', None)
        account_email = self.get_argument('account', None)
        password = self.get_argument('password', None)
        result = login_lib(self, account_user, account_email, password)
        if result['status'] == 200:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})



class RegistHandler(BaseHandler):
    """用户注册"""
    def get(self):
        return self.render('account/sign-up.html')

    def post(self):
        name = self.get_argument('yourname')
        password = self.get_argument('password1')
        password1 = self.get_argument('password2')
        email = self.get_argument('email')
        print name,password,password1,email
        result = personal_login_lib(self, name, password, password1, email)
        if result['status'] == 200:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})

class EmailConfirmHandler(BaseHandler):
    """邮箱链接注册"""
    def get(self):
        email = self.get_argument('email', '')
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        code_time = self.get_argument('code_time', '')
        result = regist_email_lib(self, email, username, password, code_time)
        if result['status'] is True:
            return self.write(result['msg'])
        return self.write(result['msg'])

class ForgetHandler(BaseHandler):
    """找回密码"""
    def get(self):
        return self.render('account/forgot.html')

    def post(self):
        code = round(time.time(), 2)
        email = self.get_argument('email')
        result = forget_lib(self, code, email)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class SendEmailHandler(BaseHandler):
    """发送找回密码邮件"""
    def get(self):
        code = self.get_argument('code', '')
        e_mail = self.get_argument('e_mail', '')
        print e_mail
        if e_mail is None:
            return self.render('back_end/admin-404.html')
        if code is None:
            return self.render('back_end/admin-404.html')
        if self.conn.get("found_password:%s" % e_mail) == code:
            return self.render('account/found_password.html', code=code, e_mail=e_mail)
        return self.render('back_end/admin-404.html')


class FoundpasswordHandler(BaseHandler):
    """找回密码"""
    def post(self):
        code = self.get_argument('code', '')
        e_mail = self.get_argument('e_mail', '')
        pd1 = self.get_argument('password1', '')
        pd2 = self.get_argument('password2', '')
        if pd1 == '' or pd2 == '':
            return self.write({'status': 400, 'msg': '请输入密码'})
        if pd1 != pd2:
            return self.write({'status': 400, 'msg': '两次输入的密码不一致'})
        if self.conn.get("found_password:%s" % e_mail) != code:
            return self.write({'status': 400, 'msg': '您可能在进行非法测试，我们将会对您的ip地址进行监测'})
        user = User.by_email(e_mail)
        user.password = pd1
        self.db.add(user)
        self.db.commit()
        self.conn.delete("found_password:%s" % e_mail)
        return self.write({'status': 200, 'msg': '修改密码成功'})

class IndexHandler(BaseHandler):
    """首页"""
    def get(self):
        return self.render('article/article_index.html')
