# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models

from datetime import datetime

from users.models import UserProfile
from courses.models import Course


# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11, verbose_name=u'手机号')
    course_name = models.CharField(max_length=50, verbose_name=u'课程名称')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name


class CourseComment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    course = models.ForeignKey(Course, verbose_name=u'课程名称')
    comment = models.CharField(max_length=200, verbose_name=u'评论内容')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name



class UserCollection(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    collection_id = models.IntegerField(default=0, verbose_name=u'数据id')
    collection_type = models.IntegerField(choices=((1, u'课程'), (2, u'机构'), (3, u'讲师')), default=1, verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u'消息接收者')
    message = models.CharField(max_length=500, verbose_name=u'消息内容')
    status = models.BooleanField(default=False, verbose_name=u'消息状态')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程名称')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '用户学习课程信息'
        verbose_name_plural = verbose_name
