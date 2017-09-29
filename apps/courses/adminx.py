# _*_ coding: utf-8 _*_
__author__ = 'ymfsder'
__date__ = u'2017/9/16 下午2:41'

import xadmin
from .models import Course, Lesson, Video, CourseResource, BannerCourse
from organization.models import CourseOrg


class CourseAdmin(object):
    list_display = ['name', 'desc', 'degree', 'learn_times', 'students', 'collection_num', 'image', 'click_num',
                    'add_time', 'get_zj_nums']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'collection_num', 'image',
                     'click_num']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'collection_num', 'image',
                   'click_num']
    ordering = ['-click_num']
    readonly_fields = ['click_num', 'collection_num']
    list_editable = ['detail', 'degree']
    style_fields = {'detail': 'ueditor'}
    import_excel = True

    # exclude = ['click_num', 'collection_num']

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'degree', 'learn_times', 'students', 'collection_num', 'image', 'click_num',
                    'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'collection_num', 'image',
                     'click_num']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'collection_num', 'image',
                   'click_num']
    ordering = ['-click_num']
    readonly_fields = ['click_num', 'collection_num']

    # exclude = ['click_num', 'collection_num']

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['name', 'course', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['name', 'lesson', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(Lesson, LessonAdmin)
