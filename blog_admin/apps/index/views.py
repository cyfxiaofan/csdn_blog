from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import logout,login,authenticate
from apps.index import models
from django.contrib.auth.models import User,Permission,Group
import time,datetime



# Create your views here.
def show(request):
    if request.method == 'GET':
        # 博客总数
        blog_all_num = models.Blog.objects.filter(status=0).count()
        # 收藏总数
        collect_all = models.Collect.objects.filter(status=0)
        collect_num = 0
        for pre in collect_all:
            collect_num += len(split_model(pre.collect_blog,'list'))
        # 评论总数
        comment_num = models.Comment.objects.filter(status=0).count()
        # 用户总数
        user_num = models.Users.objects.filter(status=0).count()
        # 截止到当前时间，每个小时的发布博客数
        blog_hour_list = every_hour()
        #近一个月的博客发布数量
        blog_month_list = every_day(12)
        blog_month_list = blog_month_list[::-1]
        #今日发布博客数
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today_time = now_time[:-8] + '00:00:00'
        today_num = models.Blog.objects.filter(addtime__gte=today_time, addtime__lt=now_time, status=0).count()
        # 昨日发布博客数
        yestoday_num = blog_month_list[-2]
        # 近7天发布博客数
        last_week_list = [ int(i) for i in blog_month_list[-7:]]
        last_week_num = sum(last_week_list)
        # 最新发布的博客
        new_blog = models.Blog.objects.filter(status=0).order_by('-addtime')[:6]
        # 最新发布的评论
        new_comment = models.Comment.objects.filter(status=0).order_by('-addtime')[:6]
        # 每个博客分类下的博客数占总数的百分比
        bgcate_num_list = bgcate_all()['bgcate_num_list']
        # 博客分类统计
        bgcate_info = bgcate_all()['bgcate_dict_2']

        return render(request,'index.html',{
            'blog_all_num':blog_all_num,
            'collect_num':collect_num,
            'comment_num':comment_num,
            'user_num':user_num,
            'blog_hour_list':blog_hour_list,
            'blog_month_list':','.join(blog_month_list),
            'today_num':today_num,
            'yestoday_num':yestoday_num,
            'last_week_num':last_week_num,
            'new_blog':new_blog,
            'new_comment':new_comment,
            'bgcate_num_list':bgcate_num_list,
            'bgcate_info':bgcate_info,
        })




def every_hour():
    now_time_hour = datetime.datetime.now().hour + 1
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now_time = now_time[:-5] + '00:00'
    now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
    time_list = []
    for i in range(now_time_hour):
        last_week_date = (now_time - datetime.timedelta(hours=i)).strftime('%Y-%m-%d %H:%M:%S')
        time_list.append(last_week_date)
    blog_hour_list=[]
    for i,pre in enumerate(time_list):
        n = len(time_list)
        blog_hour_list.append(models.Blog.objects.filter(addtime__gte=time_list[n-i-1],addtime__lt=time_list[n-i-2],status=0).count())


    return blog_hour_list

def every_day(days):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today_time = now_time[:-8] + '00:00:00'
    today_time_datetime = datetime.datetime.strptime(today_time, '%Y-%m-%d %H:%M:%S')
    blog_month_list = []
    blog_month_list.append(str(models.Blog.objects.filter(addtime__gte=today_time, addtime__lt=now_time,status=0).count()))
    for i in range(days):
        last_oneday_date = (today_time_datetime - datetime.timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S')
        last_oneday_date_date = datetime.datetime.strptime(last_oneday_date, '%Y-%m-%d %H:%M:%S')
        last_twoday_date = (last_oneday_date_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        blog_month_list.append(str(models.Blog.objects.filter(addtime__gte=last_twoday_date, addtime__lt=last_oneday_date, status=0).count()))

    return blog_month_list

def bgcate_all():
    bg_all = models.Blogcates.objects.filter(status=0)
    bg_num_list = []
    for pre in bg_all:
        bg_num_list.append(models.Blog.objects.filter(status=0,bgcate=pre.id).count())
    print(bg_num_list)

    bg_all_num = sum(bg_num_list)
    bgcate_dict = dict(zip(list(bg_all),bg_num_list))
    bgcate_dict = dict(sorted(bgcate_dict.items(),key = lambda k : k[1],reverse=True))
    color_list = ['green','blue','orange','red','black']
    n = 0
    for k,v in bgcate_dict.items():
        k.count=v
        try:
            k.color=color_list[n]
        except:
            pass
        n+=1
    print(bgcate_dict)
    bgcate_dict_2 = dict((list(dict(sorted(bgcate_dict.items(),key = lambda k : k[1],reverse=True)).items())[:5]))
    bgcate_num_list = [ {'label': i.title,'value':int((e/bg_all_num)*100)} for i,e in bgcate_dict.items()]

    return {'bgcate_num_list':bgcate_num_list,'bgcate_dict_2':bgcate_dict_2}

def to_login(request):
    if request.method == "GET":
        return render(request,'login.html')
    elif request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            request.session['adminstrator'] = {'stratorname':user.username,'stratorid':user.id,'stratoremail':user.email,'superuser':user.is_superuser}
            return JsonResponse({"msg":1,'href':'/'})
        else:
            return JsonResponse({'msg':0})


def quit(request):
    logout(request)
    return render(request,'login.html')


# 封装切片函数
def split_model(mod,lx):
    '''
    :param mod: obj.zidaun
    :param lx: str or list
    :return: str or list
    '''
    if lx == 'list':
        sm_list = mod.split('|')
        return sm_list
    else:
        sm_str = '|'.join(mod)
        return sm_str