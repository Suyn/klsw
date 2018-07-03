# -*- coding: utf-8 -*-
import tornado.web

from handlers.BaseHandler.base import BaseHandler
from libs.grades.grades_lib import Grade
from libs.account.account_lib import (personal_login_lib, modify_password_lib,
                                      email_confirm_lib,
                                      modify_email_lib, modify_avatar_lib,
                                      )

class PersonalAccount(BaseHandler):
    """个人资料"""
    @tornado.web.authenticated
    def get(self):
        grade = Grade(101)
        kwargs = {
            'username': self.current_user.name,
            'useremail': self.current_user.email,
            'useravatar': self.current_user.avatar,
            'Grade': grade.after()
        }
        return self.render('back_end/admin-user.html', **kwargs)

    def post(self):
        name = self.get_argument('name', None)
        password = self.get_argument('password', None)
        password1 = self.get_argument('password1', None)
        email = self.get_argument('e-mail', None)
        result = personal_login_lib(self, name, password, password1, email)
        if result['status'] == 200:
            return self.write(result['msg'])
        return self.write(result['msg'])


class ModifyPassword(BaseHandler):
    """修改密码"""
    def post(self):
        password = self.get_argument('password', None)
        password2 = self.get_argument('password2', None)
        result = modify_password_lib(self, password, password2)
        if result['status'] == 200:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})

class ModifyEmail(BaseHandler):
    """修改邮箱"""
    def get(self):
        email = self.get_argument('e_mail')
        code_time = self.get_argument('code')
        uuid = self.get_argument('uid')
        result = email_confirm_lib(self, email, code_time, uuid)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


    """修改邮箱"""
    def post(self):
        email = self.get_argument('e-mail', None)
        result = modify_email_lib(self, email)
        if result['status'] == 200:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})

class ModifyAvatar(BaseHandler):
    """修改头像"""
    def post(self):
        avatar = self.request.files.get('user_pic', None)
        result = modify_avatar_lib(self, avatar)
        if result['status'] == 200:
            return self.redirect('/my_admin/user_account')
        return self.write(result['msg'])



