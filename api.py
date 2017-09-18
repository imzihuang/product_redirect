#coding:utf-8

from tornado.web import RequestHandler
import time
import json
from random import randint
from logic import add_redirect, get_redirect, get_redirect_info, del_redirect
from base import verify_api_login
from common.ini_client import ini_load

ser_conf = ini_load('config/service.ini')
ser_dic_con = ser_conf.get_fields('auth')
auth_code = ser_dic_con.get("code")


class RedirectHandler(RequestHandler):
    def get(self):
        name = self.get_argument('name', "")
        if not name:
            self.finish(json.dumps({'state': 1, 'message': 'name is none'}))
            return
        _ = get_redirect_info(name)
        _.update({"cur_time": int(time.time())+5})
        self.finish(json.dumps({'state': 0, 'message': 'ok', 'redirect_info': _}))


class DataRedirectHandler(RequestHandler):
    def get(self):
        limit = self.get_argument('limit')
        offset = self.get_argument('offset')
        like_url = self.get_argument("url")
        count, results = get_redirect(like_url, limit, offset)
        self.finish(json.dumps({ "total": count, "rows": results}))

class DelRedirectHandler(RequestHandler):
    @verify_api_login
    def post(self, *args, **kwargs):
        name = self.get_argument("name", "")
        _ = del_redirect(name)
        if _ != 0:
            self.finish(json.dumps({'state': 1, 'message': 'del faild'}))
            return
        self.finish(json.dumps({'state': 0, 'message': 'ok'}))


class AddRedirectHandler(RequestHandler):
    @verify_api_login
    def post(self, *args, **kwargs):
        url = self.get_argument("url", "")
        parameter = self.get_argument("parameter", "")
        if not url:
            self.finish(json.dumps({'state': 1, 'message': 'url is none'}))
            return
        _ = add_redirect(url, parameter)
        if not _:
            self.finish(json.dumps({'state': 2, 'message': 'add failed'}))
            return
        self.finish(json.dumps({'state': 0, 'message': 'ok'}))

class AuthHandler(RequestHandler):
    def post(self):
        verify_code = self.get_argument("verify_code", "")
        if verify_code != auth_code:
            self.finish(json.dumps({'state': 1, 'message': 'faild'}))
            return
        # 设置cookie
        self.set_secure_cookie("user_name", "admin", expires=time.time() + float(3600))
        self.finish(json.dumps({'state': 0, 'message': 'ok'}))

class LogoutHandler(RequestHandler):
    def post(self):
        try:
            self.clear_cookie("user_name")
            self.finish(json.dumps({'state': 0, 'message': 'logout ok'}))
        except Exception:
            self.finish(json.dumps({'state': 1, 'message': 'logout faild'}))
