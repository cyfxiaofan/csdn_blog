from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
# 取消当前函数防跨站请求伪造功能，即便settings中设置了全局中间件。
from django.views.decorators.csrf import csrf_exempt
import time, random
#时区设置模块
from django.utils import timezone
from apps.user.views import oss_func
from apps.index import models
import re

# Create your views here.
def show(request):
    upbanner = models.Banner.objects.filter(status=1,cid=0).order_by('pic_index')
    downbanner = models.Banner.objects.filter(status=0,cid=0).order_by('pic_index')
    #如果有开启状态 且 是 首页的 轮播图
    #判断是否够四张，不够的话就用 空白图片填充
    if upbanner:
        # 拿出来计数 防止多次判断的时候调用会额外的多次操作数据库
        banner_num = upbanner.count()
        if banner_num == 4:
            extra_html = ''
        elif banner_num <4:
            extra_html=''
            for banner_img in range(4-banner_num):
                extra_html +='''
                    <div class="col-md-3 img-div draggable-element">
                          <img ondblclick="delthisbanner(this)" src="http://placehold.it/500x300" name="0" class="img-responsive">
                </div>
                '''
        else:
            extra_html=''
    else:
        #说明没有图片，去哪不用空白图片填充
        extra_html=''
        for  banner_img in range(4):
            extra_html+='''
                <div class="col-md-3 img-div draggable-element">
                          <img ondblclick="delthisbanner(this)" src="http://placehold.it/500x300" name="0" class="img-responsive">
                </div>
            '''
    return render(request,'banner/banner.html',{'bannerlist':upbanner,'extra_html':extra_html,'downbanner':downbanner})


#上传图片
@csrf_exempt
def inputbannerlist(request):
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
            #存图片
            bannerinfo = models.Banner(
                pic_url=file_name,
            )
            bannerinfo.save()
            #存完之后请求id
            thisbannerid = models.Banner.objects.get(pic_url=file_name)
            previewid = thisbannerid.id
            return JsonResponse({'file_name': file_name, 'previewid': previewid})
        except Exception as e:
            file_name = ''
            print(e)
            return JsonResponse({'file_name': file_name})

    else:
        return HttpResponse('')

#删除up轮播图
def delbanner(request):
    if request.method =="POST":
        delbanner_id = request.POST.get('delbanner_id')
        print(delbanner_id)
        try:
            delbannerinfo = models.Banner.objects.get(id=delbanner_id)
            delbannerinfo.status=0
            delbannerinfo.save()
            return JsonResponse({'msg':1})
        except Exception as e:
            return JsonResponse({'msg':str(e)})
    else:
        return render(request,'404.html')

#删除down图片
def deldownbanner(request):
    if request.method =='POST':
        deldownbanner_id = request.POST.get('delbanner_id')
        try:
            delbannerinfo = models.Banner.objects.get(id=int(deldownbanner_id))
            delbannerinfo.status = 2
            delbannerinfo.save()
            return JsonResponse({'msg':1})
        except Exception as e:
            return JsonResponse({'msg':str(e)})
    else:
        return render(request,'404.html')

#启用--更新
def updatabanner(request):
    if request.method =="POST":
        blogurl = request.POST.get('blogurl','')
        blogtitle = request.POST.get('blogtitle','')
        picid = request.POST.get('picid','')
        try:
            pic_obj = models.Banner.objects.get(id = picid)
            pic_obj.blog_url = blogurl
            pic_obj.blog_title = str(blogtitle)
            print(blogtitle)
            pic_obj.save(force_update=True)
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'信息不完整'})
        img_id_1=int(request.POST.get('img_id_1'))
        img_id_2=int(request.POST.get('img_id_2'))
        img_id_3=int(request.POST.get('img_id_3'))
        img_id_4=int(request.POST.get('img_id_4'))
        img_list = [img_id_1,img_id_2,img_id_3,img_id_4]
        n=0
        try:
            for img_id in img_list:
                if img_id:
                    bannerinfo = models.Banner.objects.get(id=img_id)
                    bannerinfo.status=1
                    bannerinfo.pic_index=n
                    n+=1
                    bannerinfo.save()
            return JsonResponse({'msg':1})
        except Exception as e:
            return JsonResponse({'msg':str(e)})
    else:
        return render(request,'404.html')
#更新按钮
def update_up_banner(request):
    if request.method =="POST":
        img_id_1=int(request.POST.get('img_id_1'))
        img_id_2=int(request.POST.get('img_id_2'))
        img_id_3=int(request.POST.get('img_id_3'))
        img_id_4=int(request.POST.get('img_id_4'))
        img_list = [img_id_1,img_id_2,img_id_3,img_id_4]
        n=0
        try:
            for img_id in img_list:
                if img_id:
                    bannerinfo = models.Banner.objects.get(id=img_id)
                    bannerinfo.status=1
                    bannerinfo.pic_index=n
                    n+=1
                    bannerinfo.save()
            return JsonResponse({'msg':1})
        except Exception as e:
            return JsonResponse({'msg':str(e)})


#checkblogurl
def checkurl(request):
    if request.method == 'GET':
        blogurl = request.GET.get('blogurl','')
        if not blogurl:
            return JsonResponse({'msg':0,'errormsg':'操作太快，请重新输入！'})
        blog_dict = check_blogurl(blogurl)
        try:
            user_obj = models.Users.objects.get(userid=blog_dict['userid'])
            blog_obj = models.Blog.objects.get(id=blog_dict['blogid'])
            if blog_obj.uid.id == user_obj.id :
                return JsonResponse({'msg':1,'blog_title':blog_obj.title})
            else:
                return JsonResponse({'msg':0,'errormsg':'未找到博客信息！'})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':0,'errormsg':'未找到博客信息！'})

def getblogdetail(request):
    if request.method == 'GET':
        picid = request.GET.get('picid')
        try:
            pic_obj = models.Banner.objects.get(id=picid)
            blog_url = pic_obj.blog_url
            blog_title = pic_obj.blog_title
            return JsonResponse({'msg':1,'blogurl':blog_url,'blogtitle':blog_title})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':0})



# check blog_url
def check_blogurl(url):
    try:
        url = url+'/'
        userid = re.findall('user_(.*?)/',url)[0]
        blogid = re.findall('blog_(.*?)/',url)[0]
        return {'userid':userid,'blogid':blogid}
    except Exception as e:
        print(e)
        return JsonResponse({'msg':0,'errormsg':'未找到博客信息！'})




