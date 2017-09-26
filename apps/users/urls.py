# _*_ coding: utf-8 _*_
__author__ = 'ymfsder'
__date__ = '2017/9/25 下午5:06'

from django.conf.urls import url
from .views import UserCenterInfoView, UserCourseView, ImageUploadView, ResetPwdView, SendEmailCodeView, UpdateEmail, \
    UserFavCourseView, UserFavTeacherView, UserFavOrgView, UserMessageView

urlpatterns = [
    url(r'^user_info/$', UserCenterInfoView.as_view(), name='user_info'),
    url(r'^user_course/$', UserCourseView.as_view(), name='user_course'),
    url(r'^image/upload/$', ImageUploadView.as_view(), name='image_upload'),
    url(r'^reset/pwd/$', ResetPwdView.as_view(), name='reset_pwd'),
    url(r'^send_email_code/$', SendEmailCodeView.as_view(), name='send_email_code'),
    url(r'^update_email/$', UpdateEmail.as_view(), name='update_email'),
    # 用户收藏课程
    url(r'^user_fav_course/$', UserFavCourseView.as_view(), name='user_fav_course'),
    # 用户收藏讲师
    url(r'^user_fav_teacher/$', UserFavTeacherView.as_view(), name='user_fav_teacher'),
    # 用户收藏机构
    url(r'^user_fav_org/$', UserFavOrgView.as_view(), name='user_fav_org'),
    # 用户消息
    url(r'^user_message/$', UserMessageView.as_view(), name='user_message'),

]
