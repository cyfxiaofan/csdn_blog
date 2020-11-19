from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from apps.index import models
from apps.user.oss_img import oss_func
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
import time,random
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

def show(request):
	if request.method == "GET":
		keywords = request.GET.get('keywords')
		if keywords:
			search_user = models.Users.objects.filter(
				Q(id__contains=keywords)|
				Q(username__contains=keywords)|
				Q(phone__contains=keywords)|
				Q(userid__contains=keywords)
			)
		else:
			search_user = models.Users.objects.all()
		if not search_user:
			search_user=models.Users.objects.all()
		for everyperson in search_user:
			if everyperson.viptime == None:
				everyperson.viptime = '未开通'
			else:
				if float(everyperson.viptime) < time.time():
					everyperson.viptime = '已到期'
				else:
					everyperson.viptime = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(float(everyperson.viptime)))
		#分页
		paginator=Paginator(search_user,10)
		p=int(request.GET.get('page',1))
		totalpages = paginator.num_pages
		rankpagelist = paginator.page(p)
		return render(request,'user/user.html',{'userinfo':rankpagelist,'totalpages':totalpages,'keywords':keywords})





def adduser(request):
	if request.method == 'GET':
		pass
		return render(request,'user/adduser.html')
	elif request.method == 'POST':
		username = request.POST.get('username','')
		phone = request.POST.get('phone','')
		password = request.POST.get('password','')
		repassword = request.POST.get('repassword','')
		head_url = request.POST.get('head_url','')
		if (not all([username,phone,password,repassword,head_url]) or password != repassword):
			return render(request,'user/adduser.html',{'jscode': 'function showSuccessMessages(){swal("添加失败!", "用户信息不完整", "error");}showSuccessMessages()',})
		#处理密码
		password = make_password(password,'None','pbkdf2_sha256')
		#生成随机用户ID 
		while True:
			userid = str(random.randint(100000,999999))
			this_user = models.Users.objects.filter(userid=userid).count()
			if not this_user :
				break
		try:
			new_user = models.Users(
					userid=userid,
					username=username,
					phone=phone,
					password=password,
					head_url=head_url,
				)
			new_user.save(force_insert=True)
			ZL_obj = models.Zhuanlan(
				uid=new_user,
				title='默认专栏',
			)
			ZL_obj.save(force_insert=True)
			return render(request,'user/adduser.html',{
					'jscode': 'function showSuccessMessages(){swal("添加成功!", "用户信息已添加，用户ID为：'+userid+'", "success");}showSuccessMessages()',
				})
		except Exception as e:
			return render(request,'user/adduser.html',{
					'jscode': 'function showSuccessMessages(){swal("添加失败!", '+str(e)+', "error");}showSuccessMessages()',
				})
	else:
		return render(request,'404.html')


#用户禁用
def delthis(request):
	if request.method == 'POST':
		i_id = request.POST.get('i_id','')
		status = request.POST.get('status','')
		print(i_id,status)
		if not all([i_id,status]):
			return JsonResponse({'msg':'出错了···请稍后重试'})
		thisuser = models.Users.objects.get(id=i_id)
		try:
			thisuser.status = int(status)
			thisuser.save(force_update=True)
		except Exception as e:
			print(str(e))
			return JsonResponse({'msg':'出错啦，请联系管理员处理'})
		if int(status) == 1:

			return JsonResponse({'msg':1,'successmsg':'该账号已被禁用'})
		else:
			return JsonResponse({'msg':1,'successmsg':'该账号已被解封'})
	else:
		return render(request,'404.html')


#用户编辑
def edituser(request):
	if request.method == 'POST':
		uid = request.POST.get('uid','')
		uname = request.POST.get('uname','')
		uphone = request.POST.get('uphone','')
		uhead_url = request.POST.get('uhead_url','')
		if not all([uid,uname,uphone,uhead_url]):
			return JsonResponse({'msg':'信息不完整！'})
		editobj = models.Users.objects.get(id=uid)
		if not editobj:
			return JsonResponse({'msg':'找不到该用户！'})
		try:
			editobj.username = uname
			editobj.phone = uphone
			editobj.head_url = uhead_url
			editobj.save(force_update=True)
		except Exception as e:
			print(str(e))
			return JsonResponse({'msg':'修改失败，请联系管理员处理！'})
		return JsonResponse({'msg':1})
	else:
		return render(request,'404.html')

#服务器处理图片返回网络地址
#跳过csrf_token验证
@csrf_exempt
def updatauser(request):
	if request.method == 'POST':
		#取年月日   防止重名为图片命名
		year = time.strftime('%Y', time.localtime(int(time.time())))
		month = time.strftime('%m', time.localtime(int(time.time())))
		day = time.strftime('%d', time.localtime(int(time.time())))
		try:
			path = "article/" + year + '/' + month + '/' + day + '/'
			f = request.FILES.get('file')
			file_name = path + str(random.randint(1000000, 9999999)) + str(int(time.time())) + f.name

			# 请求并拼接图片地址
			from urllib.request import urljoin
			#阿里云  oss 对图片处理成网络地址
			oss_func(fileobj=f.read(), filepath=file_name)
			file_name = urljoin('http://jiamengweb.oss-cn-beijing.aliyuncs.com', file_name)
		except Exception as e:
			print(str(e))
			file_name = ''
		return JsonResponse({'file_name':file_name})
	else:
		return HttpResponse('')

