# -*- coding: utf-8 -*-
from personal_acount_handler import (PersonalAccount, ModifyPassword,
                                     ModifyEmail, ModifyAvatar)

my_account_handlers = [
    (r'/my_admin/user_account', PersonalAccount),
    (r'/my_admin/modify_pd', ModifyPassword),
    (r'/my_admin/modify_email', ModifyEmail),
    (r'/my_admin/modify_avatar', ModifyAvatar),
]