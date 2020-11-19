from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from apps.blog import views
from apps.index import models
import time,datetime
# Create your views here.

# 检查用户是否登录
def checklogin_alert(func):
    def inner(request):
        # 是 POST 说明是在发表评论
        if request.method == 'POST':
            try:
                user_session = request.session.get('userinfo')
                user_id = user_session['userid']
                if not user_id:
                    return HttpResponse("<script>alert('请先登录!');history.back(-1)</script>")
                else:
                    return func(request)
            except Exception as e:
                return HttpResponse("<script>alert('请先登录!');history.back(-1)</script>")
        else:
            return func(request)
    return inner

@checklogin_alert
def show(request):
    if request.method == 'GET':
        user_id = views.login_or_false(request)
        if user_id:
            user_obj = models.Users.objects.get(id=user_id)
            user_jf = user_obj.yl_2
            if not user_jf:
                user_jf = 0
            if user_obj.viptime == None:
                user_obj.viptime = '未开通'
            else:
                if float(user_obj.viptime) < time.time():
                    user_obj.viptime = '已到期'
                else:
                    user_obj.viptime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(float(user_obj.viptime)))
        else:
            user_obj = {}
            user_jf = 0
            user_obj['viptime'] = '未开通'

        return render(request,'vip.html',{'user_obj':user_obj,'user_jf':user_jf})
    elif request.method == 'POST':
        user_id = views.login_or_404(request)
        try:
            user_id = int(user_id)
        except:
            return user_id
        user_obj = models.Users.objects.get(id=user_id)
        vipdays = int(request.POST.get('vipdays',''))
        try:
            vnum = int(user_obj.yl_2)
        except:
            vnum = 0
        if vnum >= vipdays:
            try:
                # 更新用户的积分
                user_obj.yl_2 = str(int(user_obj.yl_2) - vipdays)
                # 延长用户的vip时间
                if (not user_obj.viptime) or float(user_obj.viptime) < time.time()   :
                    viptime = delay_time(time_num=time.time(),days=vipdays)
                else:
                    # vip 到期时间 = 当前vip 到期时间+ 充值的天数
                    viptime = delay_time(time_num=user_obj.viptime,days=vipdays)
                user_obj.viptime = viptime
                user_obj.save(force_update=True)
                return redirect('/vip',{
                                    'jscode':'layer.msg("充值成功")',
                                })
            except Exception as e:
                return redirect('/vip', {
                    'jscode':'layer.msg("充值失败")',
                })
        else:
            user_id = views.login_or_false(request)
            if user_id:
                user_obj = models.Users.objects.get(id=user_id)
                user_jf = user_obj.yl_2
                if not user_jf:
                    user_jf = 0
                if user_obj.viptime == None:
                    user_obj.viptime = '未开通'
                else:
                    if float(user_obj.viptime) < time.time():
                        user_obj.viptime = '已到期'
                    else:
                        user_obj.viptime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(float(user_obj.viptime)))
            else:
                user_obj = {}
                user_jf = 0
                user_obj['viptime'] = '未开通'

            return render(request, 'vip.html', {'user_obj': user_obj, 'user_jf': user_jf,'jscode':'layer.msg("积分不足,充值失败")',})






#时间戳处理函数
def delay_time(time_num,days):
    '''
    :param time_num: 时间戳
    :param days: 要推迟的天数
    :return: 推迟之后时间戳
    '''
    try:
        new_viptime = str(datetime.datetime.fromtimestamp(float(time_num)) + datetime.timedelta(days=int(days)))[:-7]
        time_tuple = time.strptime(new_viptime, '%Y-%m-%d %H:%M:%S')
        viptime = str(time.mktime(time_tuple))
    except Exception as e:
        print(e)
        new_viptime = str(datetime.datetime.fromtimestamp(float(time_num)) + datetime.timedelta(days=int(days)))
        time_tuple = time.strptime(new_viptime, '%Y-%m-%d %H:%M:%S')
        viptime = str(time.mktime(time_tuple))
    return viptime


