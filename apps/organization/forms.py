# _*_ coding: utf-8 _*_
__author__ = 'ymfsder'
__date__ = '2017/9/22 上午10:05'
import re

from django import forms


from operation.models import UserAsk


# 用户咨询
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE="^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p =re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码格式不正确',code='mobile_invalid')




