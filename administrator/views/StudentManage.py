from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from django.conf import settings    # 获取 settings.py 里边配置的信息
import os
import json
from index.models import *
import xlrd, xlwt
from django.db.models import Avg,Min,Sum,Max,Count


def login(request):

    return HttpResponse("Hello World Administrator!!!!")


def student_manage(request):
    data = UserInfo.objects.all()
    print(" student_manage  data--------", type(data))
    content = {'data': data}
    # print("info_manage  ", content)
    return render(request, '../templates/admin/student_manage.html', content)


@csrf_exempt
def batch_add_student(request):
    print("batch_add_student  ", request.FILES["file"])
    st_file = request.FILES["file"]
    fname_list = os.listdir(settings.DATA_ROOT)
    for f in fname_list:
        if st_file.name == f:
            print("文件未上传")
            res = {'code': 0, 'msg': '上传失败。文件重名，若要上传请重命名', 'data': 1}
            return HttpResponse(json.dumps(res))
    fname = os.path.join(settings.DATA_ROOT, st_file.name)
    try:
        with open(fname, 'wb') as file:
            for c in st_file.chunks():
                file.write(c)
        print("文件已上传")
        excel_to_databases(st_file)
        res = {'code': 0, 'msg': '上传成功', 'data': 1}
        return HttpResponse(json.dumps(res))
    except Exception as e:
        print(e)
        return HttpResponse("0")


#  excel数据导入数据库
def excel_to_databases(the_file):
    if the_file:
        print("excel_to_databases-----------  excel数据导入数据库")
        f = the_file.read()
        data = xlrd.open_workbook(file_contents=f)
        names = data.sheet_names()  # 返回表格中所有工作表的名字
        for sheet_name in names:
            status = data.sheet_loaded(sheet_name)  # 检查sheet1是否导入完毕
            if status is True:
                table = data.sheet_by_name(sheet_name)
                try:
                    keys = table.row_values(2)  # 第二行作为key值
                except Exception as e:
                    print(e)  # 表格中存在空sheet，或者第一行没数据
                    continue
                if keys:
                    rowNum = table.nrows  # 获取该sheet中的有效行数
                    colNum = table.ncols  # 获取该sheet中的有效列数
                    if rowNum == 0 or colNum == 0:
                        continue
                    else:
                        for i in range(3, rowNum):  # 从第三行（数据行）开始取数据
                            sheet_data = []  # 定义一个列表用来存放对应数据
                            for j in range(colNum):  # j对应列值
                                sheet_data.append(table.row_values(i)[j])  # 把第i行第j列的值取出赋给第j列的键值，构成字典
                                print("result--------", sheet_data)
                            print(sheet_data[4])
                            User.objects.create(phone_id=int(sheet_data[4]), user_password="0000")
                            user_phone = User.objects.get(phone_id=int(sheet_data[4]))
                            department = Department.objects.get(id=1)
                            UserInfo.objects.create(user_id=int(sheet_data[1]), user_name=sheet_data[2],
                                                    user_specialty=sheet_data[3], user_phone=user_phone,
                                                    user_qq=int(sheet_data[5]), user_organization=sheet_data[6],
                                                    department=department, user_college="信息科学与技术学院", user_instructor=sheet_data[9])
        message = "success"
    else:
        message = "failed"
    return message


# 3.1.查 - name
def search_student(request):
    st_id = request.GET['st_id']
    student = UserInfo.objects.get(user_id=st_id)
    content = {'data': student}
    return render(request, '../templates/admin/student_manage.html', content)


# 3.2.查 - id
def search_student_id(request, student_id):
    student = UserInfo.objects.filter(user_id=student_id)
    content = {'data': student}
    return render(request, '../templates/admin/edit_student.html', content)


def edit_student(request):
    pass


def delete_student(request, student_id):
    res = User.objects.filter(userinfo__user_id=student_id).delete()
    print("delete_student-------:success")
    return redirect('/admin/student_manage')