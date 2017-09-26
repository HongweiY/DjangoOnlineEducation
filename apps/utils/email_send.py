# _*_ coding: utf-8 _*_
__author__ = 'ymfsder'
__date__ = '2017/9/19 下午3:40'
from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from OnlineEducation.settings import EMAIL_FROM


def random_str(random_length=8):
    str = ''
    chars = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


# 发送注册邮件
def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'ymfsder-注册邮件'
        email_body = u'请点击下面邮件完成注册：http://127.0.0.1:8000/activate/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = 'ymfsder-找回密码'
        email_body = u'请点击下面邮件找回密码：http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == 'update_email':
        email_title = 'ymfsder-修改邮箱'
        email_body = u'你的邮箱验证码为：{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
