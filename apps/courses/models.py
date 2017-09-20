# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models

from datetime import datetime


# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'课程名称')
    desc = models.CharField(max_length=100, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(max_length=6, choices=(('low', u'初级'), ('mid', u'中级'), ('high', u'高级')),
                              verbose_name='难度')
    learn_times = models.IntegerField(default=0,verbose_name=u'学习时长单位分钟')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    collection_num = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name=u'课程封面图')
    click_num = models.IntegerField(default=0, verbose_name=u'课程点击数量')
    add_time = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'课程添加时间')

    class Meta:
        verbose_name = u'章节信息'
        verbose_name_plural = verbose_name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节名称')
    name = models.CharField(max_length=100, verbose_name=u'视频名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'视频添加时间')

    class Meta:
        verbose_name = u'视频信息'
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'课程资源名称')
    download = models.FileField(upload_to='course/resource/%Y/%d', verbose_name=u'课程对应的资源名称', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'课程资源添加时间')

    class Meta:
        verbose_name = u'课程资源信息'
        verbose_name_plural = verbose_name
