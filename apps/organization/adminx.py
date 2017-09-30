# _*_ coding: utf-8 _*_
__author__ = 'ymfsder'
__date__ = '2017/9/16 下午3:53'
import xadmin
from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'add_time', 'desc']
    model_icon = 'fa fa-map-marker'


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'address', 'city', 'category', 'collection_num', 'click_num', 'image', 'add_time']
    search_fields = ['name', 'desc', 'collection_num', 'category', 'click_num', 'image', 'address', 'city']
    list_filter = ['name', 'desc', 'collection_num', 'category', 'click_num', 'image', 'address', 'city', 'add_time']
    relfield_style = 'fk_ajax'
    model_icon = 'fa fa-university'


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years', 'work_company', 'collection_num', 'work_position', 'click_num',
                    'feature', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'collection_num', 'work_position', 'click_num',
                     'feature']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'collection_num', 'work_position', 'click_num',
                   'feature', 'add_time']
    model_icon='fa fa-user-md'


xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
