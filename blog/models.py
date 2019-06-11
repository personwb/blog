# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import paginator

from django.db.models.signals import post_save, post_delete

from django.dispatch import receiver

from django.db import models


class User(models.Model):

    username = models.CharField(max_length=32,
                                null=True,
                                verbose_name='用户名称')

    email = models.EmailField(verbose_name='email')

    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name='创建时间')

    gender = models.CharField(max_length=1,
                              default='0',
                            verbose_name='性别')

    mobile_phone = models.CharField(max_length=11,
                                    verbose_name='手机号')

    def to_obj(self):
        return {
            'name': self.username,
            'phoneNum': self.mobile_phone
        }


try:
    User.objects.get(pk=1)
except:
    User().save()
