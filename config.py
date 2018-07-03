# -*- coding: utf-8 -*-
settings = dict(
    login_url='/user_login',
    cookie_secret='abcdefghijklmnopqrstuvwxyz',
    debug=True,
    template_path='templates',
    static_path='static',
    xsrf_cookies=True,
    pycket={
            'engine': 'redis',
            'storage': {
                'host': 'localhost',
                'port': 6379,
                'db_sessions': 5,
                'db_notifications': 11,
                'max_connections': 2**31,
            },
            'cookies': {
                'expires_days': 1,
                'max_age': 3600
            }
        }
)
