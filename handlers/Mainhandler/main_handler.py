# -*- coding: utf-8 -*-
from handlers.BaseHandler.base import BaseHandler
import functools
# @tornado.web.authenticated

def authpermission(fun):
    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        if self.current_user is not None and self.current_user.name == 'suyn':
            return fun(self, *args, **kwargs)
        else:
            return self.render('back_end/admin-404.html')
    return wrapper


class AdminIndexHandler(BaseHandler):
    """Admin首页"""
    @authpermission
    def get(self):
        kwargs = {
            'current_user': self.current_user,
        }
        return self.render('back_end/admin-index.html', **kwargs)

class Error404Handler(BaseHandler):
    def get(self):
        return self.render('back_end/admin-404.html')