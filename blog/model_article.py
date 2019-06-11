# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import datetime

from enum import Enum


class ArticleNodeType(Enum):

    Directory = 'directory'

    DirectoryArticle = 'directory_article'

    Article = 'article'

    Root = 'root'


class ArticleContentType(Enum):

    MD = 'mark_down_file'

    HTML = 'html_file'

    Route = 'route_path'

    NONE = 'none'


def article_md_upload_to(instance, filename):

    time_format = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    return 'artical/%s/%s.md' % (instance.no, time_format)


def article_html_upload_to(instance, filename):

    time_format = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    return 'artical/%s/%s.html' % (instance.no, time_format)


class Article(models.Model):

    no = models.CharField(max_length=20, default='no', db_index=True, verbose_name='文章编号')

    node_type = models.CharField(max_length=50, default='directory', verbose_name='节点属性')

    s_node = models.ForeignKey(to='Article', null=True, verbose_name='父级节点')

    root_node = models.BooleanField(default=False, verbose_name='是否是根节点')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    order = models.BigIntegerField(default=0, verbose_name='顺序')

    scan = models.BigIntegerField(verbose_name='浏览次数', default=0)

    title = models.CharField(max_length=1000, default='标题', null=True, verbose_name='标题')

    thumbnail_text = models.CharField(null=True, max_length=100, verbose_name='缩略文本')

    content_type = models.CharField(default='none', max_length=30, verbose_name='内容类型')

    mark_down_file = models.FileField(upload_to=article_md_upload_to, null=True, verbose_name='markdown路径')

    html_file = models.FileField(upload_to=article_html_upload_to, null=True, verbose_name='html文件路径')

    route_path = models.CharField(null=True, max_length=200, verbose_name='路由路径')


ArticleNoCache = None


class ArticleNo(models.Model):

    no = models.BigIntegerField(default=1, verbose_name='当前编号')

    @classmethod
    def get_no(cls):
        global ArticleNoCache
        ArticleNoCache = ArticleNo.objects.all().first()
        if not ArticleNoCache:
            ArticleNoCache = ArticleNo.objects.create()
            ArticleNoCache.save()
            return ArticleNoCache.no
        ArticleNoCache.no += 1
        ArticleNoCache.save()
        return ArticleNoCache.no
