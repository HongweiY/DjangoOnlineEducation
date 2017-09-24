# _*_ coding: utf-8 _*_
__author__ = 'ymfsder'
__date__ = '2017/9/24 下午9:47'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """
    用户登录验证
    """

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
