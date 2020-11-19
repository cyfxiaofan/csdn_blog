from django.shortcuts import render
from django.http import JsonResponse
from apps.index import models
import time
import datetime


# Create your views here.

def show(request):
    if request.method == 'GET':
        return render(request,'vip/vip.html')
    elif request.method == 'POST':
        vipdays = request.POST.get('vipdays','')
        user_id = request.POST.get('user_id','')
        if not all([vipdays,user_id]):
            return JsonResponse({'msg':0,'errormsg':'信息不完整或有误！'})
        try:
            vipuser_obj = models.Users.objects.get(userid=user_id)
            #  当前用户的viptime时间戳 小于当前 说明vip已到期
            #  当前用户的viptime时间戳 为空 说明vip未开通过
            # vip 到期时间 = 当前时间+充值的天数
            if (not vipuser_obj.viptime) or float(vipuser_obj.viptime) < time.time()   :
                viptime = delay_time(time_num=time.time(),days=vipdays)
            else:
                # vip 到期时间 = 当前vip 到期时间+ 充值的天数
                viptime = delay_time(time_num=vipuser_obj.viptime,days=vipdays)
            vipuser_obj.viptime = viptime
            vipuser_obj.save(force_update=True)
            return render(request,'vip/vip.html',{
                    'jscode': 'function showSuccessMessages(){swal("充值成功!", "VIP时间已充值成功", "success");}showSuccessMessages()',
                })
        except Exception as e:
            print(e)
            return render(request,'vip/vip.html',{
                    'jscode': 'function showSuccessMessages(){swal("充值失败!", "请联系管理员处理", "error");}showSuccessMessages()',
                })


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