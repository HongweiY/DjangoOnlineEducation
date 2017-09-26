# _*_ encoding:utf-8 _*_register.html
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponse
from pure_pagination import Paginator, PageNotAnInteger
from .models import UserProfile, EmailVerifyRecord

from .forms import LoginForm, RegisterForm, ForgetPwdForm, ResetForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserCollection, UserMessage
from courses.models import Course, Teacher, CourseOrg


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用户登录
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': u' 用户暂未激活'})
            else:
                return render(request, 'login.html', {'msg': u'用户名密码不正确！'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


# 用户注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {'register_form': register_form, 'msg': u'用户已存在，请直接登录 '})
            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()
            # 写入欢迎祖册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = u'欢迎注册ymfsder教育在线'
            user_message.save()

            send_register_email(username, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


# 激活用户
class ActivateUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'activate_error.html')
        return render(request, 'login.html')


# 找回密码：
class ForgetPasswordView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                send_register_email(email, 'forget')
                return render(request, 'send_success.html')
            else:
                return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg': u'系统中不存在该用户！'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'activate_error.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    # 重置密码
    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get('password', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '两次密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'reset_form': reset_form})


class UserCenterInfoView(LoginRequiredMixin, View):
    """
    用户个人中心
    """

    def get(self, request):
        user_info = request.user
        return render(request, 'usercenter-info.html', {
            'user_info': user_info

        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class ImageUploadView(LoginRequiredMixin, View):
    """
    用户修改个人图像
    """

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"修改失败"}', content_type='application/json')


class ResetPwdView(View):
    # 重置密码
    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get('password', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(reset_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """

    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmail(LoginRequiredMixin, View):
    """
    用户修改邮箱
    """

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        exit_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if exit_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class UserCourseView(LoginRequiredMixin, View):
    """
    用户课程中心
    """

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,

        })


class UserFavCourseView(LoginRequiredMixin, View):
    """
    用户收藏的课程
    """

    def get(self, request):
        user_fav_course = UserCollection.objects.filter(user=request.user, collection_type=1)
        user_fav_course_ids = [user_fav_course_id.collection_id for user_fav_course_id in user_fav_course]
        all_fav_courses = Course.objects.filter(id__in=user_fav_course_ids)
        return render(request, 'usercenter-fav-course.html', {
            'all_fav_courses': all_fav_courses
        })


class UserFavTeacherView(LoginRequiredMixin, View):
    """
    用户收藏讲师
    """

    def get(self, request):
        user_fav_teacher = UserCollection.objects.filter(user=request.user, collection_type=3)
        user_fav_teacher_ids = [user_fav_teacher_id.collection_id for user_fav_teacher_id in user_fav_teacher]
        all_fav_teachers = Teacher.objects.filter(id__in=user_fav_teacher_ids)
        return render(request, 'usercenter-fav-teacher.html', {
            'all_fav_teachers': all_fav_teachers
        })


class UserFavOrgView(LoginRequiredMixin, View):
    """
    用户收藏机构
    """

    def get(self, request):
        user_fav_org = UserCollection.objects.filter(user=request.user, collection_type=2)
        user_fav_org_ids = [user_fav_org_id.collection_id for user_fav_org_id in user_fav_org]
        all_fav_orgs = CourseOrg.objects.filter(id__in=user_fav_org_ids)
        return render(request, 'usercenter-fav-org.html', {
            'all_fav_orgs': all_fav_orgs
        })


class UserMessageView(LoginRequiredMixin, View):
    """
    用户信息
    """

    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        message_num = UserMessage.objects.filter(user=request.user.id, status=False)
        # 课程机构进行分页
        p = Paginator(all_messages, 5, request=request)
        all_messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'all_messages': all_messages,
            'message_num': message_num,
        })
