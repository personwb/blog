# -*- coding: utf-8 -*-

import json
import logging
import uuid

from common.exception.CodeMsgException import CodeMsgException, CodeMsgEmptyException

from common.response import res_cross, res

from models import User

logger = logging.getLogger("default")


def getToken():
    return uuid.uuid4()


def money_fen_to_y(money):
    '''
    分转化为元
    :param money: 金额（分）int
    :return: 金额（元）float
    '''
    return money / 100.0


def money_y_to_fen(money):
    '''
    元转化为分
    :param money: 金额（元）float
    :return: 金额（分）int
    '''
    # 1. 保证两位小数
    s = '%.2f' % float(money)

    # 2 转整数
    return int(float(s) * 100)


def request_log(fn):
    def p_request(*args):
        request = args[0]
        try:
            logger.info('\nget rquest：\nbody: %s\nmethod: %s\nscheme: %s\npath: %s\n content_type: %s' % (
            request.body, request.method, request.scheme, request.path, request.content_type))
        except Exception as e:
            logger.info(e)
        return fn(*args)
    return p_request


# trans request body to dict
def trans_dict_body(fn):

    def p_trans_dict_body(*args):

        request = args[0]

        method = request.method

        content_type = request.content_type

        if method == 'GET':
            body = request.GET
        else:
            body = request.body
            try:
                body = json.loads(body)
            except Exception as e:
                logger.info(e)
                body = {}

        args = args + (body,)

        return fn(*args)

    return p_trans_dict_body


# trans request body to dict
def check_token_multi_form(fn):

    def p_trans_dict_body(*args):

        request = args[0]

        method = request.method

        content_type = request.content_type

        files = {}

        if content_type == 'multipart/form-data':
            body = request.POST or request.GET
            files = request.FILES
        elif method == 'GET':
            body = request.GET
        else:
            body = request.body
            try:
                body = json.loads(body)
            except Exception as e:
                logger.info(e)
                body = {}

        args = args + (User.objects.get(pk=1), body, files)

        return fn(*args)

    return p_trans_dict_body


# check token and return user_id
def check_token(fn):

    def p_check_token(*args):

        request = args[0]

        method = request.method

        content_type = request.content_type

        if method == 'GET':
            body = request.GET
        else:
            body = request.body
            try:
                body = json.loads(body)
            except Exception as e:
                logger.info(e)
                body = {}

        args = args + (User.objects.get(pk=1), body,)

        return fn(*args)

    return p_check_token


def catch_exception_response(fn):

    def catch_exception(*args):

        try:
            result = fn(*args)
        except CodeMsgEmptyException as empty:
            return res(empty.code, None, empty.message)
        except CodeMsgException as empty:
            return res(empty.code, None, empty.message)
        return result

    return catch_exception


def catch_exception_response_cross(fn):

    def catch_exception(*args):

        try:
            result = fn(*args)
        except CodeMsgEmptyException as empty:
            return res_cross(empty.code, None, empty.message)
        except CodeMsgException as empty:
            return res_cross(empty.code, None, empty.message)
        return result

    return catch_exception


def get_key(obj, key):

    if not obj or not isinstance(obj, dict) or not obj.get(key, None):
        raise CodeMsgEmptyException('未获取到' + key)

    return obj[key]