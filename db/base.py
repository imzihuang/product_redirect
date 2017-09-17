#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta
import simplejson
from datetime import datetime
import threading
from common.ini_client import ini_load

_conf=ini_load('config/mysql.ini')
_dic_con=_conf.get_fields('product_db')

connect = 'mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(
    _dic_con.get('user'),
    _dic_con.get('password'),
    _dic_con.get('host'),
    _dic_con.get('port', 3306),
    _dic_con.get('database')
)


#Base = declarative_base(bind=engine)

_LOCK = threading.Lock()
_FACADE = None


def _create_facade_lazily():
    global _LOCK
    with _LOCK:
        global _FACADE
        if _FACADE is None:
            args = {
                "encoding": "utf8",
                "convert_unicode": True
            }
            _FACADE = EngineFacade(
                connect,
                **args
            )

        return _FACADE

def get_engine():
    facade = _create_facade_lazily()
    return facade.get_engine()


def get_session():
    facade = _create_facade_lazily()
    return facade.get_session()

class EngineFacade():
    def __init__(self, connect, **kwargs):
        self.connect = connect
        self.kwargs = kwargs

    def get_engine(self):
        engine = create_engine(connect, **self.kwargs)
        return engine

    def get_session(self):
        engine = create_engine(connect, **self.kwargs)
        Session = sessionmaker(bind=engine)
        return Session()

class DateJsonEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__()
        return simplejson.JSONEncoder.default(self, obj)

class AlchemyEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                try:
                    data = unicode(obj.__getattribute__(field))
                    simplejson.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except Exception:
                    fields[field] = None
            # a json-encodable dict
            return fields

        if isinstance(obj, datetime):
            return obj.__str__()
        return simplejson.JSONEncoder.default(self, obj)

def json_dumps_time(json,**kwargs):
    """
    获取json串，带time
    :param json:
    :param kwargs:
    :return:
    """
    return simplejson.dumps(json,cls=DateJsonEncoder, **kwargs)

def json_dumps_alchemy(json,**kwargs):
    return simplejson.dumps(json, cls=AlchemyEncoder, **kwargs)

def json_load(str_json):
    return simplejson.loads(str_json)