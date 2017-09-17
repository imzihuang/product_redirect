#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado import httpserver
from tornado.web import URLSpec, StaticFileHandler, Application
from tornado.options import define, options
from tornado.ioloop import IOLoop
from setproctitle import setproctitle
import views
import api
from settings import *


def view_handlers():
    prefix = default_settings.get('product_prefix', '/product')
    if prefix[-1] != '/':
        prefix += '/'

    return [
        URLSpec('/', views.RedirectHandler, default_settings),
        URLSpec('/manage.html', views.HomeHandler, default_settings),
        URLSpec('/(?P<id_>[a-f\d]{12})', views.RedirectHandler, default_settings),
        (prefix + r'(.*\.(css|png|gif|jpg|js|ttf|woff|woff2|map))', StaticFileHandler, {'path': default_settings.get('static_path')}),
    ]

def api_handlers():
    return [
        ('/get_redirect', api.RedirectHandler),
        ('/get_data', api.DataRedirectHandler),
        ('/del_data', api.DelRedirectHandler),
        ('/add_data', api.AddRedirectHandler)
    ]

class My_Application(Application):
    def __init__(self, handlers=None, default_host="", **settings):
        super(My_Application, self).__init__(view_handlers() + api_handlers() + handlers, default_host, **settings)

def make_app():
    settings = {
        'cookie_secret': "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    }
    return My_Application([], **settings)

define("port", default=9090, help="run on the given port", type=int)
setproctitle('product:redirect')

if __name__ == "__main__":
    options.logging = 'info'
    app = make_app()
    server = httpserver.HTTPServer(app, xheaders=True)
    server.bind(options.port)
    server.start(0)
    IOLoop.instance().start()

    #app.listen(options.port)
    #tornado.ioloop.IOLoop.current().start()
