#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.log_client import gen_log
from db.base import get_session
from db import api
from db import models
import time
import random
from common.ini_client import ini_load

ser_conf = ini_load('config/service.ini')
ser_dic_con = ser_conf.get_fields('service')
ser_url = ser_dic_con.get("url")
ser_port = ser_dic_con.get("port")



def verify_redirect(session, url="", parameter=""):
    """
    验证重复
    :return: 0:没有重复；1: 重复
    """
    try:
        query = api.model_query(session, "Redirect", {"url": [url], "parameter": [parameter]})
        if query.count() > 0:
            return 1
        return 0
    except Exception as ex:
        gen_log.error("get available redirect error:%r"%ex)
        raise ex

def get_redirect(like_url, limit, offset):
    """
    模糊查询，产品主题
    :param product_keyword:
    :return:
    """

    try:
        session = get_session()
        if like_url:
            query = session.query(models.Redirect).filter(models.Redirect.url.like("%"+like_url+"%"))
        else:
            query = api.model_query(session, "Redirect", {})
        all_count = query.count()
        results = query.offset(offset).limit(limit).all()
        _results = []
        for result in results:
            _ = result.to_dict()
            redirect_url = "http://%(ip)s:%(port)s/%(name)s"%{
                "ip": ser_url,
                "port": ser_port,
                "name": _.get('name'),
            }
            _.update({"redirect_url" : redirect_url})
            _results.append(_)

        return all_count, _results
    except Exception as ex:
        gen_log.error("like query redirect error: %r"% ex)
        return 0, []
    finally:
        session.close()

def get_redirect_info(name):
    try:
        session = get_session()

        query = api.model_query(session, "Redirect", {"name": [name]})
        result = query.first()
        return result.to_dict()
    except Exception as ex:
        gen_log.error("get redirect error: %r"% ex)
        return {}
    finally:
        session.close()

def add_redirect(url, parameter):
    """
    新增路径
    :return:
    """
    try:
        session = get_session()
        if verify_redirect(session, url, parameter):
            return False
        name = str(int(time.time())) + str(random.randint(0, 99)).zfill(2)

        redirect = {
            "url": url,
            "parameter": parameter,
            "name": name
        }
        model_redirect = api.convert_model("Redirect", redirect)
        session.add(model_redirect)
        session.commit()
        return True
    except Exception as ex:
        gen_log.error("add redirect error:%r"%ex)
        return False
    finally:
        session.close()

def del_redirect(name):
    """
    删除
    :param name:
    :return:
    """
    try:
        session = get_session()
        query = api.model_query(session, "Redirect", {"name": [name]})
        query.delete(synchronize_session=False)
        session.commit()
        return 0
    except Exception as ex:
        gen_log.error("del user error:%r"%ex)
        return 1
    finally:
        session.close()