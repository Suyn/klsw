# -*- coding: utf-8 -*-
import tornado.web
from pycket.session import SessionMixin
from libs.db.dbsession import dbSession
from libs.redis_connect.redis_conn import conn
from module.account.user_account import User


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def initialize(self):
        self.db=dbSession
        self.conn=conn
        self.flashes = None

    def get_current_user(self):
        """获取当前用户"""
        username = self.session.get("user_name")
        user = None
        if username:
            user = User.by_name(username)
        return user if user else None

        # if username:
        #     user = users[username['user_tablename']].by_id(username['user_id'])
        #     return user if user else None
        # else:
        #     return None

    def on_finish(self):
        self.db.close()