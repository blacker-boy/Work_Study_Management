from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from django.conf import settings    # 获取 settings.py 里边配置的信息
import os
import json, time
from index.models import *
import xlrd, xlwt
from django.db.models import Avg,Min,Sum,Max,Count


def free_time_index(request):

    return render(request, '../templates/admin/free_time.html')


@csrf_exempt
def batch_add_freetime(request):  # 将空闲时间表导入数据库
    if request.method == 'POST':
        ft_content = json.loads(request.POST["ft_content"])
        print(ft_content, type(ft_content))
        table_name = ft_content['table_name']
        data_week = ft_content['data_week']

        table_name_list = FreeTimeTableInfo.objects.all().values("table_name")
        for t_name in table_name_list:
            if table_name == t_name["table_name"]:
                week_list = extract_ftime_database(table_name)
                msg = "表名重复，请重命名"
                res = {'code': 0, 'msg': msg, 'data': week_list}
                return HttpResponse(json.dumps(res))
        FreeTimeTableInfo.objects.create(table_name=table_name)
        data = {}
        for day in data_week:
            data.update(day)
        try:
            for i in range(5):
                for j in range(6):
                    day = str(i+1) + str(j+1)
                    peoples = data[day].rstrip("\n").split("\n")
                    print(peoples)
                    for name in peoples:  # 存数据库
                        if name == "":
                            continue
                        student_id = UserInfo.objects.get(user_name=name)
                        table_info_id = FreeTimeTableInfo.objects.get(table_name=table_name)
                        StudentFreeTime.objects.create(free_time=day, student=student_id, table_info=table_info_id)
            msg = "保存成功"
            res = {'code': 0, 'msg': msg, 'data': 1}
            return HttpResponse(json.dumps(res))
        except Exception as e:
            print(e)
            msg = "保存失败"
            res = {'code': 0, 'msg': msg, 'data': 1}
            return HttpResponse(json.dumps(res))


# 从数据库读出空闲时间并分组
def extract_ftime_database(args):
    table_name = args
    res = StudentFreeTime.objects.filter(table_info__table_name=table_name).values("id", "free_time", "student", "table_info")
    week_list = []
    for i in range(5):
        day_list = {}
        for j in range(6):
            day = str(i + 1) + str(j + 1)
            name_list = ""
            for f_time in res:
                if f_time["free_time"] == day:
                    student_id = f_time["student"]
                    name = UserInfo.objects.filter(user_id=student_id).values("user_name")
                    name_list = name_list + name[0]["user_name"] + "\n"
            day_list[day] = name_list
        week_list.append(day_list)
    print("extract_ftime_database---- week_list:  ", week_list)
    return week_list


# 上传空闲时间excel表
@csrf_exempt
def import_freetime(request):
    print("batch_add_student  ", request.FILES["file"])
    st_file = request.FILES["file"]
    fname_list = os.listdir(settings.DATA_ROOT)
    for f in fname_list:
        if st_file.name == f:
            print("文件未上传")
            table_data = extract_ftime_excel(st_file)
            res = {'code': 0, 'msg': '上传失败。文件重名，若要上传请重命名', 'data': table_data}
            return HttpResponse(json.dumps(res))
    fname = os.path.join(settings.DATA_ROOT, st_file.name)
    try:
        with open(fname, 'wb') as file:
            for c in st_file.chunks():
                file.write(c)
        print("文件已上传")
        table_data = extract_ftime_excel(st_file)
        res = {'code': 0, 'msg': '上传成功', 'data': table_data}
        return HttpResponse(json.dumps(res))
    except Exception as e:
        print(e)
        return HttpResponse("0")


# 从excel提取空闲时间
def extract_ftime_excel(the_file):
    if the_file:
        print("extract_ftime_excel-----------  从excel提取空闲时间")
        the_file.seek(0)
        f = the_file.read()
        data = xlrd.open_workbook(file_contents=f)
        table_data = {}
        names = data.sheet_names()  # 返回表格中所有工作表的名字
        for sheet_name in names:
            status = data.sheet_loaded(sheet_name)  # 检查sheet1是否导入完毕
            if status is True:
                table = data.sheet_by_name(sheet_name)
                rowNum = table.nrows  # 获取该sheet中的有效行数
                colNum = table.ncols  # 获取该sheet中的有效列数
                table_name = table.row_values(0)[0]
                print("extract_ftime_excel-----table_name: ", table_name)
                if rowNum == 0 or colNum == 0:
                    continue
                else:
                    table_content = {}
                    for i in range(1, colNum):
                        sheet_data = []
                        for j in range(2, rowNum):
                            sheet_data.append(table.row_values(j)[i])  # 把第i行第j列的值取出赋给第j列的键值，构成字典
                        table_content["day"+str(i)] = sheet_data
                    print("extract_ftime_excel----------- table_data ", json.dumps(table_content))
                    table_data["table_name"] = table_name
                    table_data["table_content"] = table_content
                    return table_data
        message = "success"
    else:
        message = "failed"
    return message


def shifts_manage(request):
    print("shifts_manage-----")
    return render(request, '../templates/admin/shifts_manage.html')


def duty_manage(request):
    print("duty_manage-----")
    return render(request, '../templates/admin/duty_manage.html')


def log_manage(request):
    print("log_manage-----")
    return render(request, '../templates/admin/log_manage.html')


def salary_manage(request):
    print("salary_manage-----")
    return render(request, '../templates/admin/salary_manage.html')


def performance_manage(request):
    print("performance_manage-----")
    return render(request, '../templates/admin/performance_manage.html')


def upload_resource(request):
    print("upload_resource-----")
    return render(request, '../templates/admin/upload_resource.html')


def file_backup(request):
    print("file_backup-----")
    return render(request, '../templates/admin/file_backup.html')