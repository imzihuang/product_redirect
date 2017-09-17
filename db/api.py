#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from sqlalchemy.sql import func
import models
from common.log_client import gen_log

def convert_model(class_name, info_dic):
    """
    字典->model
    :param class_name:
    :param info_dic:
    :return:
    """
    try:
        class_model = getattr(models, class_name)
        model = class_model()
        for k,v in info_dic.iteritems():
            setattr(model, k, v)
        return model
    except Exception as ex:
        gen_log.error("%s convert error: %r"%(class_name, ex))

def model_query(session, class_name, query_dict):
    """
    通用查询，单元测试ut
    :param session:
    :param class_name: 实体名
    :param query_dict: 查询条件，格式：{'device_name':['FWQSB'], 'device_sn':['27350626']}
    :return: query
    """
    try:
        class_model = getattr(models, class_name)
        query = session.query(class_model)
        for key, value in query_dict.iteritems():
            column_name = getattr(class_model, key)
            query = query.filter(getattr(column_name, 'in_')(value))
        return query
    except Exception as ex:
        gen_log.error("%s query error: %r"%(class_name, ex))
        raise ex




