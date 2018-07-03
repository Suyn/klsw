# -*- coding: utf-8 -*-
from account_handler import (LoginHandler, RegistHandler, ForgetHandler,
                             EmailConfirmHandler, FoundpasswordHandler,
                             SendEmailHandler)

account_handlers = [
    (r'/user_login', LoginHandler),
    (r'/user_regist',  RegistHandler),
    (r'/user_found_pd',  ForgetHandler),
    (r'/send_forget_email',  SendEmailHandler),
    (r'/email_confirm',  EmailConfirmHandler),
    (r'/found_password',  FoundpasswordHandler),
]