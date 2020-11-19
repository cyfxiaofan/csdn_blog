from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.hashers import make_password
from django.db.models import Q


# Create your views here.
# 检查权限
def checkpermission_alert(func):
    def inner(request,*args, **kwargs):
        adminstrator = request.session.get('adminstrator')
        if adminstrator:
            if int(adminstrator['superuser']) == 1:
                return func(request,*args, **kwargs)
            else:
                return HttpResponse("<script>alert('您的权限不足!');history.back(-1)</script>")
        else:
            return HttpResponse("<script>alert('您的权限不足!');history.back(-1)</script>")
    return inner

@checkpermission_alert
def show(request):
    if request.method == "GET":
        keywords = request.GET.get('keywords','')
        if keywords:
            adminuser = User.objects.filter(
                Q(id__contains=keywords) |
                Q(username__contains = keywords) |
                Q(email__contains = keywords)
            )
        else:
            adminuser = User.objects.all()

        return render(request,'perssion/perssion.html',{
            'adminuser':adminuser
        })


@checkpermission_alert
def adminuseradd(request):
    if request.method == "GET":
        return render(request,'perssion/addperssion.html')
    elif request.method =="POST":
        is_super = int(request.POST.get('is_super',0))
        username =request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get("email")
        if is_super:
            adminuser = User.objects.create_superuser(username,email,password)
        else:
            adminuser = User.objects.create_user(username,email,password)
        adminuser.save()

        return render(request,'perssion/addperssion.html',{
            "jscode":"swal('添加管理员成功！','管理员信息已生效！','success')",
        })



@checkpermission_alert
def checkadminperssionuser(reqeust):
    if reqeust.method == "GET":
        adminperssionusername = reqeust.GET.get('adminusername')
        adminuser = User.objects.filter(username = adminperssionusername).count()
        if adminuser:
            return JsonResponse({"msg":0})
        else:
            return JsonResponse({"msg":1})


#编辑按钮ajax所请求数据
@checkpermission_alert
def edit_this(request):
    if request.method == "POST":
        editid = request.POST.get('editid','')
        if editid == '':
            return JsonResponse({'msg':'服务器繁忙，请稍后重试'})
        edituser = User.objects.get(id=editid)
        if not edituser:
            return JsonResponse({'msg':'找不到该用户'})
        # 请求数据： 用户名  是否超级管理员  邮箱  组
        username = edituser.username
        is_superuser = edituser.is_superuser
        email = edituser.email
        # 拼接组的下拉选项  并为当前组添加 selected 属性
        # 获取该用户所添加的所有组！ 因为是下拉框所设置的权限，所以限制该用户的组只能有一个
        # 尝试所点击的对象所有用的 组名

        return JsonResponse({
            'username':username,
            'is_superuser':is_superuser,
            'email':email,
        })

@checkpermission_alert
def edit_submit(request):
    if request.method == "POST":
        uid = request.POST.get('uid','')
        if uid == '':
            return JsonResponse({'msg':"服务器繁忙请稍后重试"})
        strator = User.objects.get(id=uid)
        if not strator:
            return JsonResponse({'msg':'找不到该用户'})
        strator.username = request.POST.get('uname')
        strator.email = request.POST.get('uemail')
        strator.is_superuser = int(request.POST.get('is_super'))
        strator.save()
        return JsonResponse({"msg":1})

@checkpermission_alert
def delthis(request):
    if request.method == 'POST':
        delid = request.POST.get('delid','')
        if delid == '':
            return JsonResponse({'msg':'服务器繁忙'})
        deluser = User.objects.get(id=delid)
        if not deluser:
            return JsonResponse({'msg':'要删除的对象不存在'})
        try:
            deluser.delete()
            return JsonResponse({"msg":1})
        except Exception as e:
            return JsonResponse({"msg":str(e)})

@checkpermission_alert
def resetpwd(request):
    if request.method == "POST":
        resetid = request.POST.get('resetid','')
        if resetid == '':
            return JsonResponse({'msg':'服务器繁忙'})
        resetuser = User.objects.get(id=resetid)
        if not resetuser:
            return JsonResponse({'msg':'要重置的对象不存在'})
        try:
            resetuser.password=make_password('123456',None,'pbkdf2_sha256')
            resetuser.save()
            return JsonResponse({'msg':1})
        except Exception as e:
            return JsonResponse({'msg':str(e)})





