# _*_ coding: utf-8 _*_
__author__ = 'ymfsder'
__date__ = '2017/9/16 下午3:33'
import xadmin

from .models import UserAsk, CourseComment, UserCollection, UserMessage, UserCourse


class UserAskAdmin(object):
    list_display = ['mobile', 'name', 'add_time', 'course_name']
    search_fields = ['mobile', 'name', 'course_name']
    list_filter = ['mobile', 'name', 'add_time', 'course_name']


class CourseCommentAdmin(object):
    list_display = ['user', 'course', 'add_time', 'comment']
    search_fields = ['user', 'course', 'comment']
    list_filter = ['user', 'course', 'add_time', 'comment']


class UserCollectionAdmin(object):
    list_display = ['user', 'collection_id', 'add_time', 'collection_type']
    search_fields = ['user', 'collection_id', 'collection_type']
    list_filter = ['user', 'collection_id', 'add_time', 'collection_type']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'add_time', 'status']
    search_fields = ['user', 'message', 'status']
    list_filter = ['user', 'message', 'add_time', 'status']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
