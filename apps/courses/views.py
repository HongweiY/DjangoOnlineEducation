# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponse
from operation.models import UserCollection, CourseComment, UserCourse
from .models import Course, CourseResource, Video
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q


# Create your views here.


class CourseListView(View):
    """
    课程列表
    """

    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        # 热门课程
        hot_courses = all_courses.order_by('-students')[:3]
        # 课程搜索
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_courses = all_courses.filter(Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword) | Q(
                detail__icontains=search_keyword))

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_courses = all_courses.order_by('-click_num')
        if sort == 'students':
            all_courses = all_courses.order_by('-students')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    """
    课程详情页
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()
        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            relate_course = []

        is_course_collection = False
        is_org_collection = False
        if request.user.is_authenticated():
            if UserCollection.objects.filter(user=request.user, collection_id=course.id, collection_type=1):
                is_course_collection = True
        if request.user.is_authenticated():
            if UserCollection.objects.filter(user=request.user, collection_id=course.course_org.id, collection_type=2):
                is_org_collection = True

        return render(request, 'course-detail.html', {
            'course': course,
            'relate_course': relate_course,
            'is_course_collection': is_course_collection,
            'is_org_collection': is_org_collection,
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程视频
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 课程点击量
        course.students += 1
        course.save()
        all_resources = CourseResource.objects.filter(course_id=int(course_id))
        # 记录用户学习过得课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_course]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]
        return render(request, 'course-video.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,

        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    课程品论
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course_id=int(course_id))
        all_comments = CourseComment.objects.filter(course_id=int(course_id))
        user_courses = UserCourse.objects.filter(course=course)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]
        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'all_comments': all_comments,
            'relate_courses': relate_courses

        })


class AddCommentView(View):
    """
    添加课程评论
    """

    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        # 判断用户是否品论过

        is_comment = CourseComment.objects.filter(course_id=course_id, user=request.user)
        if is_comment:
            return HttpResponse('{"status":"fail","msg":"您已经评论过该课程"}', content_type='application/json')
        else:
            if course_id > 0 and comments:
                course_comment = CourseComment()
                course = Course.objects.get(id=int(course_id))
                course_comment.course = course
                course_comment.comment = comments
                course_comment.user = request.user
                course_comment.save()
                return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')


class VideoPlayView(LoginRequiredMixin, View):
    """
    课程视频播放
    """

    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        course = video.lesson.course

        # 记录用户学习过得课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_course]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video': video

        })
