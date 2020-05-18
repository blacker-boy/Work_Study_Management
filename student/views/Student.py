from django.shortcuts import render, HttpResponse, redirect


def login(request):
    print("login-----")
    return redirect("/student/station_apply")


def station_apply(request):
    print("station_apply-----")
    return render(request, '../templates/student/station_apply.html')


def shifts_sign(request):
    print("shifts_sign-----")
    return render(request, '../templates/student/shifts_sign.html')


def achievement(request):
    print("achievement-----")
    return render(request, '../templates/student/achievement.html')


def down_resource(request):
    print("down_resource-----")
    return render(request, '../templates/student/down_resource.html')


def write_log(request):
    print("down_resource-----")
    return render(request, '../templates/student/write_log.html')
