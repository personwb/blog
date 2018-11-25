# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

import os

import uuid

from django.core.files import File

from mysite.settings import MEDIA_ROOT

from common.utils import parse_to_url

from common.md import md2html

from common.response import res_cross_success, res_cross

from .views_common import request_log, check_token, catch_exception_response, get_key, check_token_multi_form

from .model_artical import ArticalLevelTwo, ArticalLevelOne, Artical, ArticalNo

logger = logging.getLogger('default')


@request_log
@catch_exception_response
@check_token
def artical_list(request, user, body):

    result = [item.to_obj_with_level_two_list() for item in ArticalLevelOne.objects.all().order_by('-order')]

    for level_one in result:
        for level_two in level_one['levelTwoList']:
            level_two['articalList'] = [artical.simple_to_obj() for artical in Artical.objects.filter(level_two_id=level_two['id']).order_by('-create_time')]

    return res_cross_success(result)

@request_log
@catch_exception_response
@check_token
def level_one_list(request, user, body):
    return res_cross_success([item.to_obj() for item in ArticalLevelOne.objects.all().order_by('-order')])


@request_log
@catch_exception_response
@check_token
def level_one_two_list(request, user, body):
    return res_cross_success([item.to_obj_with_level_two_list() for item in ArticalLevelOne.objects.all().order_by('-order')])


@request_log
@catch_exception_response
@check_token
def add_level_one(request, user, body):

    title = get_key(body, 'title')

    ArticalLevelOne(user=user, title=title).save()

    return res_cross_success(None)


@request_log
@catch_exception_response
@check_token
def level_one_detail(request, user, body):

    level_one_id = get_key(body, 'id')

    try:
        level_one = ArticalLevelOne.objects.get(pk=level_one_id)
    except Exception as e:
        logger.info(e)
        return res_cross('1001', None, '未查询到详情')

    return res_cross_success(level_one.to_obj())


@request_log
@catch_exception_response
@check_token
def level_two_list(request, user, body):
    return res_cross_success([item.to_obj() for item in ArticalLevelTwo.objects.all().order_by('-order')])


@request_log
@catch_exception_response
@check_token
def add_level_two(request, user, body):

    level_one_id = get_key(body, 'levelOneId')

    level_two_id = body.get('id', None)

    title = get_key(body, 'title')

    try:
        level_one = ArticalLevelOne.objects.get(pk=level_one_id)
    except Exception as e:
        logger.info(e)
        return res_cross('1001', None, '未查询到该语言')

    if level_two_id:
        try:
            level_two = ArticalLevelTwo.objects.get(pk=level_two_id)
        except Exception as e:
            logger.info(e)
            return res_cross('1001', None, '未查询到分组信息')
    else:
        level_two = ArticalLevelTwo()

    level_two.level_one = level_one
    level_two.title = title
    level_two.save()

    return res_cross_success(None)


@request_log
@catch_exception_response
@check_token
def remove_level_two(request, user, body):

    level_two_id = body.get('id', None)

    try:
        level_two = ArticalLevelTwo.objects.get(pk=level_two_id)
    except Exception as e:
        logger.info(e)
        return res_cross('1001', None, '未查询到分组信息')

    exist = Artical.objects.filter(level_two=level_two).order_by('-create_time')

    if len(exist):
        return res_cross('1001', None, '当前分组下存在文章，请先移动文章')

    level_two.delete()

    return res_cross_success(None)

@request_log
@catch_exception_response
@check_token
def level_two_detail(request, user, body):

    level_two_id = get_key(body, 'id')

    try:
        level_two = ArticalLevelTwo.objects.get(pk=level_two_id)
    except Exception as e:
        logger.info(e)
        return res_cross('1001', None, '未查询到详情')

    return res_cross_success({'detail': level_two.to_obj(), 'levelOneList': [item.to_obj() for item in ArticalLevelOne.objects.all().order_by('-order')]})


@request_log
@catch_exception_response
@check_token
def artical_manager_list(request, user, body):

    all = Artical.objects.all().order_by('-create_time')

    result = [{
        'id': artical.id,
        'title': artical.title,
        "levelOne": artical.level_two.level_one.to_obj(),
        'levelTwo': artical.level_two.to_obj(),
        'markDownFilePath': parse_to_url(artical.mark_down_file.path),
        'scan': artical.scan
    } for artical in all]

    return res_cross_success(result)


@request_log
@catch_exception_response
@check_token
def artical_detail_show(request, user, body):

    artical_id = get_key(body, 'id')

    try:
        artical = Artical.objects.get(pk=artical_id)
    except Exception as e:
        logger.info(e)
        return res_cross('1001', None, '未查询到详情')

    return res_cross_success(artical.obj_detail_scan())


@request_log
@catch_exception_response
@check_token
def artical_detail(request, user, body):

    artical_id = get_key(body, 'id')

    try:
        artical = Artical.objects.get(pk=artical_id)
    except Exception as e:
        logger.info(e)
        return res_cross('1001', None, '未查询到详情')

    return res_cross_success(artical.to_obj())


@request_log
@catch_exception_response
@check_token_multi_form
def artical_add(request, user, body, files):

    artical_id = body.get('id', None)

    artical_title = get_key(body, 'title')

    artical_level_two_id = get_key(body, 'levelTwoId')

    artical_route_path = body.get('routePath', None)

    mark_down_file = None

    if len(files):
        mark_down_file = files['file']

    try:
        level_two = ArticalLevelTwo.objects.get(pk=artical_level_two_id)
    except Exception as e:
        logger.info(e)
        return res_cross('1001', None, '未匹配到一级菜单')

    if artical_id:
        try:
            artical = Artical.objects.get(pk=artical_id)
        except Exception as e:
            artical = Artical()
            no = ArticalNo()
            no.save()
            artical.no = no
    else:
        artical = Artical()
        no = ArticalNo()
        no.save()
        artical.no = no

    content_type = None

    if artical_route_path:
        content_type = 'route_path'

    if mark_down_file or artical.mark_down_file:

        content_type = 'mark_down_file'

    artical.title = artical_title
    artical.content_type = content_type
    artical.level_two = level_two

    if mark_down_file:

        try:
            content = mark_down_file.read()
        except Exception as e:
            return res_cross('1001', None, '分析MarkDown文件失败')

        content_html = md2html(content)

        artical.mark_down_file = mark_down_file

        tmp_directory = os.path.join(MEDIA_ROOT, 'tmp')

        if not os.path.exists(tmp_directory):
            os.makedirs(tmp_directory)

        tmp_artical_directory = os.path.join(tmp_directory, 'artical')

        if not os.path.exists(tmp_artical_directory):
            os.makedirs(tmp_artical_directory)

        tmp_file = os.path.join(tmp_directory, uuid.uuid4().hex)

        html_file = open(tmp_file, 'w')
        html_file.write(content_html)
        html_file.close()

        html_read_file = File(open(tmp_file, 'r'))
        artical.html_file = html_read_file

        os.remove(tmp_file)

    artical.save()

    return res_cross_success(artical.to_obj())