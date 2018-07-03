# -*- coding: utf-8 -*-
import time
# from random import randint
import json
from module.account.user_account import User
from utils.send_email.send_email import send_qq_html_email


def login_lib(self, account_user, account_email, password):
    """用户登录"""
    if account_email is None or account_email == '':
        return {'status': 400, 'msg': '用户名/邮箱 输入为空'}
    username = User.by_name(account_user)
    email = User.by_email(account_email)
    if not username and not email:
        return {'status': 400, 'msg': '用户不存在'}
    if username and username.auth_password(password):
        username.loginnum += 1
        username.last_login = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 46800))
        self.db.add(username)
        self.db.commit()
        self.session.set('user_name', username.name)
        return {'status': 200, 'msg': '验证成功'}
    elif email and email.auth_password(password):
        email.loginnum += 1
        email.last_login = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 46800))
        self.db.add(email)
        self.db.commit()
        self.session.set('user_name', email.name)
        return {'status': 200, 'msg': '验证成功'}
    else:
        return {'status': 400, 'msg': '用户名/邮箱 或密码错误'}



def personal_login_lib(self, name, password, password1, email):
    """用户注册"""
    if name == '':
        return {'status': 400, 'msg': '姓名输入为空'}
    if password == '':
        return {'status': 400, 'msg': '密码输入为空'}
    if password1 == '':
        return {'status': 400, 'msg': '重复密码输入为空'}
    if email == '':
        return {'status': 400, 'msg': '邮箱输入为空'}
    if len(name) < 2 or len(name) > 18:
        return {'status': 400, 'msg': '姓名不足2个字符或大于18个字符'}
    if len(password) < 6 or len(password) > 64:
        return {'status': 400, 'msg': '密码不足6个字符或大于64个字符'}
    if password != password1:
        return {'status': 400, 'msg': '两次输入的密码不相等'}
    if len(email) < 7 or len(email) > 32:
        return {'status': 400, 'msg': '邮箱格式不正确'}
    username = User.by_name(name)
    if username is not None:
        return {'status': 400, 'msg': '该昵称已存在'}
    user_email = User.by_email(email)
    if user_email is not None:
        return {'status': 400, 'msg': '该邮箱已被注册'}

    code_time = round(time.time(), 2)

    user_data = {'email': email,
                 'username': name,
                 'password': password,
                 'code_time': code_time,
                 'IsSendEmail': 'no'}
    if self.conn.get("regist_email:%s" % email):
        self.conn.delete("regist_email:%s" % email)
    self.conn.setex("regist_email:%s" % email, json.dumps(user_data), 1800)
    return {'status': True, 'msg': '请注意查收您的邮件'}

def regist_email_lib(self, email, username, password, code_time):
    """注册"""
    if email == '' or email is None or username == '' or username is None or password is None or password == '' or code_time == '' or code_time is None:
        return {'status': False, 'msg': '请到页面重试'}
    regist_email = self.conn.get("regist_email:%s" % email)
    if regist_email is None:
        return {'status': False, 'msg': '请重新注册'}
    datas = json.loads(regist_email)
    if datas and str(datas['code_time']) == code_time and datas['email'] == email and datas['password'] == password and datas['username'] == username:
        user = User()
        user.name = username
        user.password = password
        user.email = email
        self.db.add(user)
        self.db.commit()
        self.conn.delete("regist_email:%s" % email)
        return {'status': True, 'msg': '注册成功'}
    return {'status': False, 'msg': '注册失败'}

def modify_password_lib(self, password, password2):
    """修改密码"""
    if password == '' or password is None:
        return {'status': 400, 'msg': '旧密码为空'}
    if password2 == '' or password2 is None:
        return {'status': 400, 'msg': '新密码为空'}
    if len(password2) < 6 or len(password2) > 64:
        return {'status': 400, 'msg': '新密码不足6个字符或大于64个字符'}
    if self.current_user.auth_password(password):
        self.current_user.password2 = password2
        self.db.commit()
        return {'status': 200, 'msg': '密码修改成功'}
    return {'status': 400, 'msg': '旧密码错误'}

def modify_email_lib(self, email):
    """修改邮箱----发送邮件"""
    if email == '' or email is None:
        return {'status': 400, 'msg': '邮箱为空'}
    if User.by_email(email) is not None:
        return {'status': 400, 'msg': '该邮箱已被绑定'}
    e_mail_list = []
    e_mail_list.append(email)
    user_uuid = self.current_user.uuid
    code_time = time.time()
    if self.conn.get("found_password:%s" % email):
        self.conn.delete("found_password:%s" % email)
    self.conn.setex("found_password:%s" % email, code_time, 1800)
    content = u"""
                    您好，<a href='http://clonesw.com'>克隆生物</a>网站提醒您，您正在进行找回密码操作,
                    修改密码请<a href="http://clonesw.com/send_forget_email?e_mail={}&code={}&uid={}">点击此链接</a>，
                    链接有效时间为30分钟，若非您本人所为请忽略此邮件。
                    """.format(email, code_time, user_uuid)
    send_qq_html_email("wedding@wulilove.cn", e_mail_list, "找回密码", content)
    return {'status': 200, 'msg': '绑定成功'}

def email_confirm_lib(self, email, code_time, uuid):
    if email is None or email == '':
        return {'status': False, 'msg': '请返回个人中心重新修改邮箱'}
    if code_time is None or code_time == '':
        return {'status': False, 'msg': '请返回个人中心重新修改邮箱'}
    user = User.by_uuid(uuid)
    if uuid is None or uuid == '' or user is None:
        return {'status': False, 'msg': '请返回个人中心重新修改邮箱'}
    data = self.conn.get("found_password:%s" % email)
    if data is None:
        return {'status': False, 'msg': '请返回个人中心重新修改邮箱'}
    if data == code_time:
        user.email = email
        self.db.commit()
        return {'status': True, 'msg': '绑定成功'}
    return {'status': False, 'msg': '请返回个人中心重新修改邮箱'}



def modify_avatar_lib(self, avatar):
    """修改头像"""
    if avatar is None or avatar == '':
        return {'status': 200, 'msg': '未选择图片'}
    avatar = avatar[0]['body']
    user = self.current_user
    try:
        user.avatar = avatar
        self.db.add(user)
        self.db.commit()
        return {'status': 200, 'msg': '头像修改成功'}
    except Exception as e:
        return {'status': 400, 'msg': e}

def forget_lib(self, code, email):
    """忘记密码"""
    if email is None or email == '':
        return {'status': False, 'msg': '邮箱为空'}
    user = User.by_email(email)
    if user is not None:
        e_mail_list = []
        e_mail_list.append(user.email)
        if self.conn.get("found_password:%s" % user.email):
            self.conn.delete("found_password:%s" % user.email)
        self.conn.setex("found_password:%s" % user.email, code, 1800)
        content = u"""
                您好，<a href='http://clonesw.com'>克隆生物</a>网站提醒您，您正在进行找回密码操作,
                修改密码请<a href="http://clonesw.com/send_forget_email?e_mail={}&code={}">点击此链接</a>，
                链接有效时间为30分钟，若非您本人所为请忽略此邮件。
                """.format(user.email, code)
        send_qq_html_email("wedding@wulilove.cn", e_mail_list, "找回密码", content)
        return {'status': True, 'msg': '发送成功，请到您的邮箱继续操作'}
    return {'status': False, 'msg': '该邮箱号码不存在'}