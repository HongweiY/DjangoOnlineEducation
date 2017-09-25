# _*_ coding: utf-8 _*_
__author__ = 'ymfsder'
__date__ = '2017/9/22 上午10:16'

from django.conf.urls import url

from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddCollectionView, \
    TeacherListView, TeacherDetailView

urlpatterns = [
    # 课程机构
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),

    url(r'^add_collection/$', AddCollectionView.as_view(), name='add_collection'),
    # 教师列表
    url(r'^teacher_list/$', TeacherListView.as_view(), name='teacher_list'),
    # 讲师详情
    url(r'^teacher_detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),

]
