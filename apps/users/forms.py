# _*_ coding: utf-8 _*_
__author__ = 'ymfsder'
__date__ = '2017/9/18 下午2:35'

from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ResetForm(forms.Form):
    password = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
