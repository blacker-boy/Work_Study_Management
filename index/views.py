from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from index.models import *
from django.db.models import Avg,Min,Sum,Max,Count
# Create your views here.


def index(request):
    return render(request, "index.html")


@csrf_exempt
def login(request):
    if request.method == 'GET':
        print("login ------GET")
        return render(request, "login.html")
    if request.method == 'POST':
        user_id = request.POST['user_id']
        password = request.POST['password']
        print("login ------id", user_id, "  password: ", password)
        try:
            user_password = User.objects.filter(phone_id=user_id).values("user_password")[0]['user_password']
            print("user_password:  ", user_password, type(user_password))
            if password == user_password:
                return redirect('/admin/student_manage')
            else:
                return HttpResponse("用户名或密码错误")
        except Exception as e:
            print(e)
            return HttpResponse("不存在该账号 ")


def register(request):
    if request.method == 'GET':
        return render(request, "register.html")
    else:
        return 0
