from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from django.conf import settings    # 获取 settings.py 里边配置的信息
import os
import json, time
from index.models import *
import xlrd, xlwt
from django.db.models import Avg,Min,Sum,Max,Count


def info_manage(request):
    print("info_manage-----")
    return render(request, '../templates/admin/info_manage.html')


def bulletin_manage(request):
    print("bulletin_manage-----")
    return render(request, '../templates/admin/bulletin_manage.html')