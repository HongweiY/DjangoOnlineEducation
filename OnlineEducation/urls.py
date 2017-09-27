# _*_ coding: utf-8 _*_
"""OnlineEducation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include

import xadmin
from django.views.static import serve
from OnlineEducation.settings import MEDIA_ROOT,STATIC_ROOT

from users.views import LoginView, RegisterView, ActivateUserView, ForgetPasswordView, ResetView, ModifyPwdView, \
    LogoutView
from users.views import IndexView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^index/', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^activate/(?P<active_code>.*)/$', ActivateUserView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetPasswordView.as_view(), name='forget'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name='reset'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构路由
    url(r'^org/', include('organization.urls', namespace='org')),
    # 课程路由
    url(r'^course/', include('courses.urls', namespace='course')),
    # 用户个人中心路由
    url(r'^user/', include('users.urls', namespace='user')),
    # 配置上传文件的访问路径
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]
# 全局404
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
