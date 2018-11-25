# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from common.utils import parse_to_url

import datetime


class ArticalLevelOne(models.Model):

    title = models.CharField(max_length=20, verbose_name='名称')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    user = models.ForeignKey(to='User', related_name='artical_one_user', verbose_name='用户')

    order = models.BigIntegerField(default=0, verbose_name='顺序')

    def to_obj(self):
        return {
            'title': self.title,
            'id': self.id
        }

    def to_obj_with_level_two_list(self):
        return {
            'title': self.title,
            'id': self.id,
            'levelTwoList': [{ 'id': two.id, 'title': two.title, } for two in ArticalLevelTwo.objects.filter(level_one_id=self.id).order_by('-order')]
        }

class ArticalLevelTwo(models.Model):

    title = models.CharField(max_length=20, verbose_name='名称')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    level_one = models.ForeignKey(to='ArticalLevelOne', related_name='artical_level_two_level_one', verbose_name='一级名称')

    order = models.BigIntegerField(default=0, verbose_name='顺序')

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

    order = models.BigIntegerField(default=0, verbose_name='顺序')

    no = models.ForeignKey(to='ArticalNo', null=True, verbose_name='文字编号')

    title = models.CharField(max_length=1000, default='标题', null=True, verbose_name='标题')

    thumbnail_text = models.CharField(null=True, max_length=100, verbose_name='缩略文本')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    content_type = models.CharField(null=True, max_length=20, verbose_name='内容类型')

    mark_down_file = models.FileField(upload_to=artical_md_upload_to, null=True, verbose_name='markdown路径')

    html_file = models.FileField(upload_to=artical_html_upload_to, null=True, verbose_name='html文件路径')

    route_path = models.CharField(null=True, max_length=200, verbose_name='路由路径')

    level_two = models.ForeignKey(to='ArticalLevelTwo', related_name='artical_level_two', verbose_name='二级名称')

    scan = models.BigIntegerField(verbose_name='浏览次数', default=0)

    def simple_to_obj(self):
        return {
            'thumbnailText': self.get_thumbnail_text(),
            'createTime': self.create_time.strftime('%Y-%m-%d %H:%M'),
            'id': self.id,
            'title': self.title,
            'contentType': self.content_type,
            'routePath': self.route_path,
            'scan': self.scan
        }

    def to_obj(self):
        html_text = None
        if self.html_file:
            with open(self.html_file.path, 'r') as r:
                html_text = r.read().decode()
                r.close()
        markDownFilePath = None
        if self.mark_down_file:
            markDownFilePath = parse_to_url(self.mark_down_file.url)
        content = ''
        # with open(self.mark_down_file.path, 'r') as r:
        #     content = r.read().decode()
        #     r.close()
        return {
            'thumbnailText': self.get_thumbnail_text(),
            'createTime': self.create_time.strftime('%Y-%m-%d %H:%M'),
            'id': self.id,
            'title': self.title,
            'htmlText': html_text,
            'levelOne': self.level_two.level_one.to_obj(),
            'levelTwo': self.level_two.to_obj(),
            "levelOneId": self.level_two.level_one.id,
            'levelTwoId': self.level_two.id,
            'markDownFilePath': markDownFilePath,
            'contentType': self.content_type,
            'routePath': self.route_path,
            'scan': self.scan,
            # 'content': content
        }

    def obj_detail_scan(self):
        self.scan = self.scan + 1
        self.save()
        return self.to_obj()

    def get_thumbnail_text(self):
        if self.thumbnail_text:
            return self.thumbnail_text
        else:
            if self.mark_down_file:
                with open(self.mark_down_file.path, 'r') as r:
                    content = r.read().decode()
                    length = len(content)
                    if length > 72:
                        valid = content[0:72]
                        self.thumbnail_text = valid.replace('\n', '')
                        self.save()
                        return valid
                    elif length == 0:
                        return ''
                    else:
                        self.thumbnail_text = content.replace('\n', '')
                        self.save()
                        return content
            else:
                return ''

class ArticalNo(models.Model):
    pass