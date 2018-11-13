# -*- coding: utf-8 -*-

from django.http import HttpResponse

from rest_framework.renderers import JSONRenderer

import logging

logger = logging.getLogger('default')


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def res_with_success(data):
    return res('200', data, 'success')

def res(code, data, message):
    logger.info('response : code: %s message: %s data: %s' % (code, message, data))
    return JSONResponse(status=200, data={
        'code': code,
        'data': data,
        'message': message
    })


def res_cross(code, data, message):
    logger.info('response with cross: code: %s message: %s data: %s' % (code, message, data))
    response = JSONResponse(status=200, data={
        'code': code,
        'data': data,
        'message': message
    })
    response["Access-Control-Allow-Origin"] = " * "
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = " * "
    return response

def res_cross_success(data=None):
    return res_cross('200', data, 'success')
