# -*- coding: utf-8 -*-
from main_handler import AdminIndexHandler, Error404Handler

from handlers.MyAcountHandler.personal_acount_url import my_account_handlers
from handlers.Account.account_url import account_handlers
from handlers.Articles.article_url import article_handlers
from handlers.Files.files_url import files_handlers

handlers = [
    (r'/my_admin/index', AdminIndexHandler),
]
handlers += my_account_handlers
handlers += account_handlers
handlers += article_handlers
handlers += files_handlers





handlers += [
    (r'.*', Error404Handler),
]
