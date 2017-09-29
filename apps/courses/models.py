# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models

from datetime import datetime

from organization.models import CourseOrg, Teacher

from DjangoUeditor.models import UEditorField


# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name=u'课程讲师', default='1')
    name = models.CharField(max_length=100, verbose_name=u'课程名称')
    category = models.CharField(max_length=20, verbose_name=u'课程分类', default='1',
                                choices=(
                                    ('1', u'前端开发'), ('2', u'后端开发'), ('3', u'移动开发'), ('4', u'数据库'), ('5', u'运维&测试')), )
    desc = models.CharField(max_length=100, verbose_name=u'课程描述')
    detail = UEditorField(verbose_name=u'详情', width=1200, height=600, imagePath="course/ueditor/",
                          filePath="course/ueditor/",
                          default='')
    degree = models.CharField(max_length=6, choices=(('low', u'初级'), ('mid', u'中级'), ('high', u'高级')),
                              verbose_name='难度')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长单位分钟')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    collection_num = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name=u'课程封面图')
    click_num = models.IntegerField(default=0, verbose_name=u'课程点击数量')

    tag = models.CharField(max_length=10, verbose_name=u'课程标签', default='')
    need_kno = models.CharField(max_length=300, verbose_name=u'课程须知', default='我知道你全都知道')
    what_learn = models.CharField(max_length=300, verbose_name=u'你能学到什么', default='能学到什么，你知道还不清楚吗？')
    tag = models.CharField(max_length=10, verbose_name=u'课程标签', default='')
    is_banner = models.BooleanField(default=False, verbose_name='是否是推荐课程')
    add_time = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获得课程章节数
        return self.lesson_set.all().count()

    get_zj_nums.short_description = '章节数'

    def get_learn_users(self):
        # 获取课程学习人数
        return self.usercourse_set.all()[:5]

    def get_lesson(self):
        # 获得全部在章节
        return self.lesson_set.all()


class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'课程添加时间')

    class Meta:
        verbose_name = u'章节信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_video(self):
        # 获得章节下的视频
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节名称')
    name = models.CharField(max_length=100, verbose_name=u'视频名称')
    url = models.CharField(max_length=200, verbose_name=u'视频路径', default='www.baidu.com')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长单位分钟')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'视频添加时间')

    class Meta:
        verbose_name = u'视频信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'课程资源名称')
    download = models.FileField(upload_to='course/resource/%Y/%d', verbose_name=u'课程对应的资源名称', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'课程资源添加时间')

    class Meta:
        verbose_name = u'课程资源信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
