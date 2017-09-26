# _*_ encoding:utf-8 _*_register.html
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from pure_pagination import Paginator, PageNotAnInteger
from .models import CityDict, CourseOrg, Teacher
from .forms import UserAskForm
from operation.models import UserCollection
from courses.models import Course
from django.db.models import Q


# Create your views here.


class OrgView(View):
    def get(self, request):
        all_cities = CityDict.objects.all()
        all_courseOrgs = CourseOrg.objects.all()
        # 课程机构搜索
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_courseOrgs = all_courseOrgs.filter(
                Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword))

        # 热门机构
        hot_orgs = all_courseOrgs.order_by('-click_num')[:3]
        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_courseOrgs = all_courseOrgs.filter(city_id=int(city_id))
        # 机构类别的筛选
        category = request.GET.get('ct', '')
        if category:
            all_courseOrgs = all_courseOrgs.filter(category=category)
        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courseOrgs = all_courseOrgs.order_by('-learn_num')
            if sort == 'courses':
                all_courseOrgs = all_courseOrgs.order_by('-course_num')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 统计符合条件的机构个数
        org_num = all_courseOrgs.count()
        # 课程机构进行分页
        p = Paginator(all_courseOrgs, 5, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html', {
            'all_cities': all_cities,
            'all_courseOrgs': orgs,
            'org_num': org_num,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
            'keywords': search_keyword
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()
        is_collection = False
        if request.user.is_authenticated():
            if UserCollection.objects.filter(user=request.user, collection_id=course_org.id, collection_type=2):
                is_collection = True
        all_course = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_course': all_course,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
            'is_collection': is_collection,
        })


class OrgCourseView(View):
    """
    机构课程
    """

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_course = course_org.course_set.all()
        is_collection = False
        if request.user.is_authenticated():
            if UserCollection.objects.filter(user=request.user, collection_id=course_org.id, collection_type=2):
                is_collection = True
        return render(request, 'org-detail-course.html', {
            'all_course': all_course,
            'course_org': course_org,
            'current_page': current_page,
            'is_collection': is_collection,
        })


class OrgDescView(View):
    """
    机构介绍
    """

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        is_collection = False
        if request.user.is_authenticated():
            if UserCollection.objects.filter(user=request.user, collection_id=course_org.id, collection_type=2):
                is_collection = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'is_collection': is_collection,
        })


class OrgTeacherView(View):
    """
    机构讲师
    """

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()
        is_collection = False
        if request.user.is_authenticated():
            if UserCollection.objects.filter(user=request.user, collection_id=course_org.id, collection_type=2):
                is_collection = True
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'current_page': current_page,
            'all_teacher': all_teacher,
            'is_collection': is_collection,
        })


class AddCollectionView(View):
    """
    用户收藏操作
    """

    def post(self, request):
        collection_id = request.POST.get('col_id', 0)
        collection_type = request.POST.get('col_type', 0)
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        exit_record = UserCollection.objects.filter(user=request.user, collection_id=int(collection_id),
                                                    collection_type=int(collection_type))
        if exit_record:
            # 取消收藏
            exit_record.delete()
            if int(collection_type) == 1:
                course = Course.objects.get(id=int(collection_id))
                course.collection_num -= 1
                if course.collection_num < 0:
                    course.collection_num = 0
                course.save()
            elif int(collection_type) == 2:
                course_org = CourseOrg.objects.get(id=int(collection_id))
                course_org.collection_num -= 1
                if course_org.collection_num < 0:
                    course_org.collection_num = 0
                course_org.save()
            elif int(collection_type) == 3:
                teacher = Teacher.objects.get(id=int(collection_id))
                teacher.collection_num -= 1
                if teacher.collection_num < 0:
                    teacher.collection_num = 0
                teacher.save()

            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            # 保存用户收藏
            user_collection = UserCollection()
            if int(collection_id) > 0 and int(collection_type) > 0:
                user_collection.user = request.user
                user_collection.collection_id = int(collection_id)
                user_collection.collection_type = int(collection_type)
                user_collection.save()
                if int(collection_type) == 1:
                    course = Course.objects.get(id=int(collection_id))
                    course.collection_num += 1
                    course.save()
                elif int(collection_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(collection_id))
                    course_org.collection_num += 1
                    course_org.save()
                elif int(collection_type) == 3:
                    teacher = Teacher.objects.get(id=int(collection_id))
                    teacher.collection_num += 1
                    teacher.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏失败"}', content_type='application/json')


class TeacherListView(View):
    """
    教师列表页
    """

    def get(self, request):
        all_teachers = Teacher.objects.all()
        # 教师搜索
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keyword) |
                Q(work_company__icontains=search_keyword) |
                Q(work_position__icontains=search_keyword))
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_num')

        # 统计教师数量
        teacher_num = all_teachers.count()
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 课程机构进行分页
        p = Paginator(all_teachers, 5, request=request)
        all_teachers = p.page(page)
        # 讲师排行榜，通过点击数量
        hot_teachers = Teacher.objects.order_by('-click_num')[:4]

        return render(request, 'teachers-list.html', {
            'all_teachers': all_teachers,
            'teacher_num': teacher_num,
            'hot_teachers': hot_teachers,
            'sort': sort,
            'keywords': search_keyword,
        })


class TeacherDetailView(View):
    """
    讲师详情页
    """

    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_num += 1
        teacher.save()
        # 该讲师的全部课程分页显示
        all_courses = Course.objects.filter(teacher=teacher)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 4, request=request)
        all_courses = p.page(page)
        # 改讲师所属机构
        course_org = CourseOrg.objects.get(teacher=teacher)
        # 讲师排行榜，通过点击数量
        hot_teachers = Teacher.objects.order_by('-click_num')[:4]
        # 判断教师是否收藏
        is_teacher_collection = False
        collection_teacher = UserCollection.objects.filter(user=request.user, collection_type=3,
                                                           collection_id=teacher.id)
        if collection_teacher:
            is_teacher_collection = True
        # 判断课程机构是否被收藏
        is_courseOrg_collection = False
        collection_courseOrg = UserCollection.objects.filter(user=request.user, collection_type=2,
                                                             collection_id=course_org.id)
        if collection_courseOrg:
            is_courseOrg_collection = True

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_courses': all_courses,
            'course_org': course_org,
            'hot_teachers': hot_teachers,
            'is_teacher_collection': is_teacher_collection,
            'is_courseOrg_collection': is_courseOrg_collection,

        })
