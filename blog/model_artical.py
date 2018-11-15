# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from common.utils import parse_to_url

import datetime


class ArticalLevelOne(models.Model):

    title = models.CharField(max_length=20, verbose_name='名称')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    user = models.ForeignKey(to='User', related_name='artical_one_user', verbose_name='用户')

    def to_obj(self):
        return {
            'title': self.title,
            'id': self.id
        }

    def to_obj_with_level_two_list(self):
        return {
            'title': self.title,
            'id': self.id,
            'levelTwoList': [{ 'id': two.id, 'title': two.title, } for two in ArticalLevelTwo.objects.filter(level_one_id=self.id)]
        }

class ArticalLevelTwo(models.Model):

    title = models.CharField(max_length=20, verbose_name='名称')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    level_one = models.ForeignKey(to='ArticalLevelOne', related_name='artical_level_two_level_one', verbose_name='一级名称')

    def to_obj(self):
        return {
            'id': self.id,
            'title': self.title,
            'levelOne': self.level_one.to_obj()
        }


def artical_md_upload_to(instance, filename):

    time_format = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    return 'artical/%d/%s.md' % (instance.no.id, time_format)


def artical_html_upload_to(instance, filename):

    time_format = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    return 'artical/%d/%s.html' % (instance.no.id, time_format)

class Artical(models.Model):

    no = models.ForeignKey(to='ArticalNo', null=True, verbose_name='文字编号')

    title = models.CharField(max_length=100, default='标题', verbose_name='标题')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    content_type = models.CharField(null=True, max_length=20, verbose_name='内容类型')

    mark_down_file = models.FileField(upload_to=artical_md_upload_to, null=True, verbose_name='markdown路径')

    html_file = models.FileField(upload_to=artical_html_upload_to, null=True, verbose_name='html文件路径')

    route_path = models.CharField(null=True, max_length=200, verbose_name='路由路径')

    level_two = models.ForeignKey(to='ArticalLevelTwo', related_name='artical_level_two', verbose_name='二级名称')

    scan = models.BigIntegerField(verbose_name='浏览次数', default=0)

    def simple_to_obj(self):
        return {
            'id': self.id,
            'title': self.title,
            'contentType': self.content_type,
            'routePath': self.route_path,
            'scan': self.scan
        }

    def to_obj(self):
        return {
            'createTime': self.create_time.strftime('%Y-%m-%d %H:%M'),
            'id': self.id,
            'title': self.title,
            'htmlText': self.html_file.file.read(),
            'levelOne': self.level_two.level_one.to_obj(),
            'levelTwo': self.level_two.to_obj(),
            "levelOneId": self.level_two.level_one.id,
            'levelTwoId': self.level_two.id,
            'markDownFilePath': parse_to_url(self.mark_down_file.url),
            'contentType': self.content_type,
            'routePath': self.route_path,
            'scan': self.scan
        }

    def obj_detail_scan(self):
        self.scan = self.scan + 1
        self.save()
        return self.to_obj()

class ArticalNo(models.Model):
    pass