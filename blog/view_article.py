# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

import os

import uuid

import datetime

from django.core.files import File

from mysite.settings import MEDIA_ROOT

from common.md import md2html

from common.response import res_cross_success, res_cross, res_cross_error

from .views_common import request_log, check_token, catch_exception_response, get_key, check_token_multi_form

from model_article import Article, ArticleNo, ArticleNodeType, ArticleContentType

import model_article_tool


logger = logging.getLogger('default')


@request_log
@catch_exception_response
@check_token
def article_list(request, user, body):
    """
    获取文章列表
    """
    return res_cross_success(model_article_tool.article_list())


@request_log
@catch_exception_response
@check_token
def article_detail(request, id, user, body):

    try:
        article = Article.objects.get(no=id)
    except Exception as e:
        logger.info(e)
        return res_cross('1001', None, '未查询到详情')

    return res_cross_success(model_article_tool.article_to_obj(article))


@request_log
@catch_exception_response
@check_token
def article_directory_create(request, user, body):
    """
    创建子文件夹
    """
    title = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    node = model_article_tool.article_by_no(body.get('sId', None))
    if not node or node.node_type != ArticleNodeType.Directory:
        return res_cross('3001', None, '异常')
    article = Article()
    article.no = ArticleNo.get_no()
    article.title = title
    article.s_node = node
    article.node_type = ArticleNodeType.Directory
    article.content_type = ArticleContentType.NONE
    article.save()
    return res_cross_success()


@request_log
@catch_exception_response
@check_token
def article_directory_update(request, user, body):
    """
    创建子文件夹
    """
    title = get_key(body, 'title')
    node = model_article_tool.article_by_no(body.get('id', None))
    node.title = title
    node.save()
    return res_cross_success()


@request_log
@catch_exception_response
@check_token
def article_delete(request, user, body):
    """
    删除文章
    """
    node = model_article_tool.article_by_no(body.get('id', None))
    if not node:
        return res_cross('3001', None, '异常')
    if Article.objects.filter(s_node=node).count():
        return res_cross_error('存在子节点，无法删除')
    node.delete()
    return res_cross_success()


@request_log
@catch_exception_response
@check_token
def article_create(request, user, body):
    """
    创建文章
    """
    s_node = model_article_tool.article_by_no(body.get('sId', None))

    if not s_node or s_node.node_type != ArticleNodeType.Directory:
        return res_cross('3001', None, '异常')

    article = Article()
    article.no = ArticleNo.get_no()
    article.title = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    article.s_node = s_node
    article.node_type = ArticleNodeType.Article
    article.save()
    return res_cross_success(model_article_tool.article_to_obj(article))


@request_log
@catch_exception_response
@check_token_multi_form
def article_update(request, user, body, files):
    """
    更新文章
    """
    article_id = body.get('id', None)

    article_title = get_key(body, 'title')

    article_route_path = body.get('routePath', None)

    mark_down_file = None

    article = None

    if article_id:
        try:
            article = Article.objects.get(no=article_id)
        except Exception as e:
            logger.info(e)
            return res_cross('1001', None, '未查询到该文章')

    if len(files):
        mark_down_file = files['file']

    content_type = ArticleContentType.NONE

    if article_route_path:
        content_type = ArticleContentType.Route

    if mark_down_file:
        content_type = ArticleContentType.MD

    article.route_path = article_route_path
    article.title = article_title
    article.content_type = content_type

    if mark_down_file:

        try:
            content = mark_down_file.read()
        except Exception as e:
            return res_cross('1001', None, '分析MarkDown文件失败')

        content_html = md2html(content)

        article.mark_down_file = mark_down_file

        tmp_directory = os.path.join(MEDIA_ROOT, 'tmp')

        if not os.path.exists(tmp_directory):
            os.makedirs(tmp_directory)

        tmp_article_directory = os.path.join(tmp_directory, 'article')

        if not os.path.exists(tmp_article_directory):
            os.makedirs(tmp_article_directory)

        tmp_file = os.path.join(tmp_directory, uuid.uuid4().hex)

        html_file = open(tmp_file, 'w')
        html_file.write(content_html)
        html_file.close()

        html_read_file = File(open(tmp_file, 'r'))
        article.html_file = html_read_file

        os.remove(tmp_file)

    try:
        article.save()
        return res_cross_success(model_article_tool.article_to_obj(article))
    except Exception as e:
        logger.error(e)
        return res_cross_error('更新失败')


