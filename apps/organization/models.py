# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models

from datetime import datetime


# Create your models here.

class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'城市名称')
    desc = models.CharField(max_length=200, verbose_name=u'城市描述')
    add_time = models.DateTimeField(datetime.now)

    class Meta:
        verbose_name = u'城市信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    idea = models.CharField(max_length=30, default='一切为了学生', verbose_name=u'机构理念', )
    desc = models.TextField(verbose_name=u'机构描述')
    category = models.CharField(max_length=20, choices=(('jg', u'培训机构'), ('gx', u'高校'), ('gr', '个人')),
                                verbose_name=u'机构类型', default='jg')
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, verbose_name=u'所在城市')
    collection_num = models.IntegerField(default=0, verbose_name=u'收藏人数')
    click_num = models.IntegerField(default=0, verbose_name=u'点击人数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name=u'机构封面图 ')
    learn_num = models.IntegerField(default=0, verbose_name='学习人数')
    course_num = models.IntegerField(default=0, verbose_name='机构课程数')

    add_time = models.DateTimeField(datetime.now)

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_teacher_nums(self):
        # 获得教师数量
        return self.teacher_set.all().count()


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u'教师所属机构')
    name = models.CharField(max_length=50, verbose_name=u'教师名称')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    age = models.IntegerField(default=0, verbose_name=u'年龄')
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50, verbose_name=u'就职公司职位')
    feature = models.CharField(max_length=30, verbose_name=u'教学特点')
    collection_num = models.IntegerField(default=0, verbose_name=u'收藏人数')
    click_num = models.IntegerField(default=0, verbose_name=u'点击人数')
    add_time = models.DateTimeField(datetime.now)
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name=u'教师图像', default='')

    class Meta:
        verbose_name = u'教师信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_course_num(self):
        return self.course_set.all().count()
