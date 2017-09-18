#!/usr/bin/python
# -*- coding: UTF-8 -*-

def verify_api_login(func):
    """
    :param func:
    :return:
    """
    def __(torn_self):
        user_name = torn_self.get_secure_cookie('user_name')
        if not user_name:
            torn_self.finish({'state': '10'})
            return
        func(torn_self)
    return __