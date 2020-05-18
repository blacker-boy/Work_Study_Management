from django.contrib import admin
from django.urls import path,re_path, include
from django.conf.urls import url, include
from administrator.views import StudentManage
from administrator.views import TaskManage
from administrator.views import InformationManage
urlpatterns = [
    url(r'^login/', StudentManage.login),
    url(r'^info_manage/', InformationManage.info_manage),
    url(r'^bulletin_manage/', InformationManage.bulletin_manage),
    url(r'^student_manage/', StudentManage.student_manage),
    url(r'search/$', StudentManage.search_student),
    url(r'get/(?P<student_id>[0-9]*)/$', StudentManage.search_student_id),
    url(r'^edit_student', StudentManage.edit_student),
    url(r'delete/(?P<student_id>[0-9]*)/$', StudentManage.delete_student),
    url(r'^batch_add_student/', StudentManage.batch_add_student),
    url(r'^free_time_manage/', TaskManage.free_time_index),
    url(r'^batch_add_freetime/', TaskManage.batch_add_freetime),
    url(r'^import_freetime/', TaskManage.import_freetime),
    url(r'^shifts_manage/', TaskManage.shifts_manage),
    url(r'^duty_manage/', TaskManage.duty_manage),
    url(r'^log_manage/', TaskManage.log_manage),
    url(r'^salary_manage/', TaskManage.salary_manage),
    url(r'^performance_manage/', TaskManage.performance_manage),
    url(r'^upload_resource/', TaskManage.upload_resource),
    url(r'^file_backup/', TaskManage.file_backup),
]
