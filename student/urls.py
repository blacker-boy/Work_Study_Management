from django.conf.urls import url, include
from student.views import Student


urlpatterns = [
    url(r'^login/', Student.login),
    url(r'^station_apply/', Student.station_apply),
    url(r'^shifts_sign/', Student.shifts_sign),
    url(r'^achievement/', Student.achievement),
    url(r'^down_resource/', Student.down_resource),
    url(r'^write_log/', Student.write_log),
]