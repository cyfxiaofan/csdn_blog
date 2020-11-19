from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
import os, time, random
from apps.index.oss_img import oss_func
from apps.index import models
import html2text as ht


# Create your views here.

# 编写装饰器检查用户是否登录
def check_login(func):
    def inner(request, *args, **kwargs):
        next_url = request.get_full_path()
        # 获取session判断用户是否已登录
        if request.session.get('userinfo'):
            # 已经登录的用户...
            return func(request, *args, **kwargs)
        else:
            # 没有登录的用户，跳转刚到登录页面
            return redirect("/login")

    return inner


@check_login
def show(request):
    if request.method == 'GET':
        edit_id = request.GET.get('editid', '')
        print(edit_id,1111111111111111111)
        user_session = request.session.get('userinfo')
        user_id = user_session['userid']
        user_obj = models.Users.objects.get(id=user_id)
        if not user_id:
            return render(request, '404.html')
        if edit_id == '':
            bgcate = models.Blogcates.objects.filter(status=0)
            zlid_obj = models.Zhuanlan.objects.filter(uid=user_obj).filter(status=0)
            return render(request, 'writeblog.html', {'blogcate': bgcate, "zlid_obj": zlid_obj})
        else:
            text_maker = ht.HTML2Text()
            text_maker.bypass_tables = False
            edit_obj = models.Blog.objects.filter(id=edit_id,status=0,uid=user_obj).first()
            # if edit_obj.source == 'csdn':
            #     html_str = edit_obj.ginfo
            #     text = text_maker.handle(html_str)
            #     md = text.split('#')  # split post content
            #     edit_obj.ginfo = md
            bgcate = models.Blogcates.objects.filter(status=0)
            user_session = request.session.get('userinfo')
            user_id = user_session['userid']
            if not user_id:
                return render(request, '404.html')
            zlid_obj = models.Zhuanlan.objects.filter(uid=user_obj).filter(status=0)
            return render(request, 'writeblog.html', {'blogcate': bgcate, "zlid_obj": zlid_obj,'edit_obj':edit_obj})


def addflzl(request):
    if request.method == 'POST':
        flzl = request.POST.get('flzl', '')
        if not flzl or flzl.isspace():
            return JsonResponse({'msg': '分类专栏不能为空'})
        user_session = request.session.get('userinfo')
        user_id = user_session['userid']
        if not user_id:
            return JsonResponse({'msg': '登录超时'})
        checkflzl = models.Zhuanlan.objects.filter(uid=models.Users.objects.get(id=user_id), title=flzl).count()
        if checkflzl:
            return JsonResponse({'msg': '该专栏已存在'})
        else:
            try:
                newzl_obj = models.Zhuanlan(
                    uid=models.Users.objects.get(id=user_id),
                    title=flzl
                )
                newzl_obj.save(force_insert=True)
                zl_html = '''
					<option value="{id}">{title}</option>
				'''.format(id=newzl_obj.id, title=newzl_obj.title)
                return JsonResponse({'msg': 1, 'zl_html': zl_html})
            except Exception as e:
                print(e)
                return JsonResponse({'msg': '添加失败，请稍后重试···'})


@check_login
def useradd_blog(request):
    if request.method == 'POST':
        blog_info = request.POST.dict()
        print(blog_info)
        if not all([blog_info['blogcate'], blog_info['blog_format'], blog_info['bloglx'],
                    blog_info['blog_flzl'], blog_info['blog_title'], blog_info['blog_bq'], blog_info['blog_content']]):
            return JsonResponse({'msg': '信息填写不完整！'})
        user_id = checkloginuser(request)
        uid_obj = models.Users.objects.get(id=user_id)
        bgcate_obj = models.Blogcates.objects.get(id=blog_info['blogcate'])
        zlid_obj = models.Zhuanlan.objects.get(id=blog_info['blog_flzl'])
        edit_id=blog_info['edit_id']
        if edit_id == 'none':
            #说明是新增博客
            try:
                useraddblog_obj = models.Blog(
                    title=blog_info['blog_title'],
                    label=blog_info['blog_bq'],
                    ginfo=blog_info['blog_content'],
                    uid=uid_obj,
                    bgcate=bgcate_obj,
                    zlid=zlid_obj,
                    ifcomment=int(blog_info['blog_format']) - 1,
                    yuanchuang=int(blog_info['bloglx']) - 1,
                    beforeurl=blog_info['before_url'],
                    source='home'
                )
                useraddblog_obj.save(force_insert=True)
                try:
                    uid_obj.yl_2 = str(int(uid_obj.yl_2)+2)
                except:
                    uid_obj.yl_2 = str(0 + 2)
                uid_obj.save(force_update=True)
                return JsonResponse({'msg': 1})
            except Exception as e:
                print(str(e))
                return JsonResponse({'msg': '网络异常！'})
        else:
            try:
            #说明是编辑博客
                update_blog_obj = models.Blog.objects.filter(id=edit_id,status=0,uid=uid_obj)
                if update_blog_obj.count() == 0:
                    return JsonResponse({'msg':'登陆失效或该博客已被删除'})
                update_blog_obj = update_blog_obj
                update_blog_obj.update(
                    title=blog_info['blog_title'],
                    label=blog_info['blog_bq'],
                    ginfo=blog_info['blog_content'],
                    uid=uid_obj,
                    bgcate=bgcate_obj,
                    zlid=zlid_obj,
                    ifcomment=int(blog_info['blog_format']) - 1,
                    yuanchuang=int(blog_info['bloglx']) - 1,
                    beforeurl=blog_info['before_url'],
                    source='home'
                )
                return JsonResponse({'msg': 2})
            except Exception as e:
                print(str(e))
                return JsonResponse({'msg': '网络异常！'})



# 验证当前是否登陆
def checkloginuser(request):
    user_session = request.session.get('userinfo')
    user_id = user_session['userid']
    if not user_id:
        return JsonResponse({'msg': '登录超时'})
    else:
        return user_id


# markdown oss上传图片和缩略图处理
from django.views.decorators.csrf import csrf_exempt
import time

@csrf_exempt
def uploadimg(request):
    if request.method == "POST":
        # ==========================================================================
        user_id = login_or_msg(request)
        user_obj = models.Users.objects.get(id=user_id)
        checkvip = check_vip(user_obj.viptime)
        if not checkvip:
            return JsonResponse({'success': 0,'message':'只有会员才可以使用上传图片功能哦！'})
        year = time.strftime('%Y', time.localtime(int(time.time())))
        month = time.strftime('%m', time.localtime(int(time.time())))
        day = time.strftime('%d', time.localtime(int(time.time())))
        try:
            path = "article/" + year + '/' + month + '/' + day + '/'
            f = request.FILES.get('editormd-image-file')
            file_name = path + str(random.randint(1000000, 9999999)) + str(int(time.time())) + f.name
            from urllib.request import urljoin
            # 阿里云  oss 对图片处理并返回网络地址
            oss_func(fileobj=f.read(), filepath=file_name)
            file_name = urljoin('http://jiamengweb.oss-cn-beijing.aliyuncs.com', file_name)
        except Exception as e:
            print(str(e))
            file_name = ''
        return JsonResponse({'success': 1, 'message': '成功', 'url': file_name})
    else:
        return JsonResponse({'success': 0, 'message': '上传失败'})


@csrf_exempt
def updatauser(request):
    if request.method == 'POST':
        # 取年月日   防止重名为图片命名
        year = time.strftime('%Y', time.localtime(int(time.time())))
        month = time.strftime('%m', time.localtime(int(time.time())))
        day = time.strftime('%d', time.localtime(int(time.time())))
        try:
            path = "article/" + year + '/' + month + '/' + day + '/'
            f = request.FILES.get('file')
            file_name = path + str(random.randint(1000000, 9999999)) + str(int(time.time())) + f.name

            # 请求并拼接图片地址
            from urllib.request import urljoin
            # 阿里云  oss 对图片处理成网络地址
            oss_func(fileobj=f.read(), filepath=file_name)
            file_name = urljoin('http://jiamengweb.oss-cn-beijing.aliyuncs.com', file_name)
        except Exception as e:
            print(str(e))
            file_name = ''
        return JsonResponse({'file_name': file_name})
    else:
        return HttpResponse('')


# 验证是否是会员
def check_vip(viptime):
    now_time = time.time()
    try:
        if float(now_time) < float(viptime):
            return True
        else:
            return False
    except:
        return False

# 验证当前是否登陆
def login_or_msg(request):
    try:
        user_session = request.session.get('userinfo')
        user_id = user_session['userid']
        if not user_id:
            return JsonResponse({'msg': '登录超时'})
        else:
            return user_id
    except Exception as e:
        return JsonResponse({'msg': '登录超时'})