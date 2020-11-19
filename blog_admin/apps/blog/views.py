from django.shortcuts import render
from apps.index import models
from django.http import JsonResponse
from apps.user.oss_img import oss_func
import time
import random
from django.core.paginator import Paginator
from django.db.models import Q



# Create your views here.


def show(request):
    if request.method == 'GET':
        keywords = request.GET.get('keywords','')
        if keywords:
            search_user = models.Users.objects.filter(Q(userid__contains=keywords)|Q(username=keywords))
            search_bgcate = models.Blogcates.objects.filter(title=keywords)
            result_blog = models.Blog.objects.filter(
                Q(id__contains=keywords) |
                Q(title__contains=keywords) |
                Q(label__contains=keywords) |
                Q(ginfo__contains=keywords) |
                Q(uid__in=list(search_user.values_list('id',flat=True))) |
                Q(bgcate__in=list(search_bgcate.values_list('id',flat=True))) |
                Q(beforeurl__contains=keywords) |
                Q(source__contains=keywords)
            )
        else:
            result_blog = models.Blog.objects.all()
        #处理数据
        for recode in result_blog:
            if recode.yuanchuang == 0:
                recode.yuanchuang = '原创'
            else:
                recode.yuanchuang = '转载'
        blogcate = models.Blogcates.objects.filter(status=0)
        paginator = Paginator(result_blog, 10)
        p = int(request.GET.get('page', 1))
        totalpages = paginator.num_pages
        rankpagelist = paginator.page(p)
        return render(request,'blog/blog.html',{'blogcate':blogcate,'result':rankpagelist,'totalpages':totalpages,'keywords':keywords})
#新增blog
def addblog(request):
    if request.method == "GET":
        blogcate = models.Blogcates.objects.filter(status=0).order_by('-list_order')
        return render(request,'blog/addblog.html',{'blogcate':blogcate})
    elif request.method == 'POST':
        blogcate = models.Blogcates.objects.filter(status=0).order_by('-list_order')
        blog_info = request.POST.dict()
        print(blog_info)
        if not all([blog_info['blogcate'],blog_info['blog_format'],blog_info['bloglx'],blog_info['user_id'],blog_info['blog_flzl'],blog_info['blog_title'],blog_info['blog_bq'],blog_info['blog_content']]):
            return render(request,'blog/addblog.html',{
                'blogcate':blogcate,
                'jscode': 'swal("添加失败!", '+'信息填写不完整'+', "error");',
            })
        try:
            addblog_obj = models.Blog(
                title=blog_info['blog_title'],
                label=blog_info['blog_bq'],
                ginfo=blog_info['blog_content'],
                bgcate=models.Blogcates.objects.get(id=blog_info['blogcate']),
                uid=models.Users.objects.get(userid=blog_info['user_id']),
                zlid=models.Zhuanlan.objects.get(id=blog_info['blog_flzl']),
                ifcomment=int(blog_info['blog_format'])-1,
                yuanchuang=int(blog_info['bloglx'])-1,
                beforeurl=blog_info['before_url'],
                source='admin',
            )
            addblog_obj.save(force_insert=True)
            return render(request,'blog/addblog.html',{
                'blogcate':blogcate,
                'jscode': 'swal("发布成功!", ' + '"博客信息已发布"' + ', "success");',
            })
        except Exception as e:
            print('$$$$$$$$$$$$$$$$$$$$'+str(e))
            return render(request,'blog/addblog.html',{
                'blogcate':blogcate,
                'jscode': 'swal("添加失败!", '+'"发生了未知的错误，请联系管理员处理"'+', "error");',
            })
#编辑博客
def edit_blog(request):
    if request.method == 'POST':
        editid = request.POST.get('editid','')
        if not editid:
            return JsonResponse({'msg':0})
        editblog_obj = models.Blog.objects.get(id=editid)
        blogcate_obj = models.Blogcates.objects.filter(status=0)
        zlid_obj = models.Zhuanlan.objects.filter(uid=editblog_obj.uid).filter(status=0)
        bgcate_html = ''
        zlid_html=''
        for recode in blogcate_obj:
            if recode.id == editblog_obj.bgcate.id:
                bgcate_html+='''
                    <option selected value="{id}">{title}</option>
                '''.format(id=recode.id,title=recode.title)
            else:
                bgcate_html +='''
                    <option  value="{id}">{title}</option>
                '''.format(id=recode.id,title=recode.title)
        for recb in zlid_obj:
            if recb.id == editblog_obj.zlid.id:
                zlid_html+='''
                    <option selected value="{id}">{title}</option>
                '''.format(id=recb.id,title=recb.title)
            else:
                zlid_html+='''
                    <option value="{id}">{title}</option>
                '''.format(id=recb.id,title=recb.title)
        #######################################
        if int(editblog_obj.ifcomment)+1 == 1:
            ifcomment_html ='''
                <option selected value="1">公开</option>
                <option value="2">私密</option>
                <option value="3">公开但禁止评论</option>
            '''
        elif int(editblog_obj.ifcomment)+1 == 2:
            ifcomment_html ='''
                <option value="1">公开</option>
                <option selected value="2">私密</option>
                <option value="3">公开但禁止评论</option>
            '''
        else:
            ifcomment_html ='''
                <option value="1">公开</option>
                <option value="2">私密</option>
                <option selected value="3">公开但禁止评论</option>
            '''
        ###########################################
        if editblog_obj.yuanchuang == 0:
            yuanchuang_html='''
                <option selected value="1">原创</option>
                <option value="2">转载</option>
            '''
        else:
            yuanchuang_html='''
                <option value="1">原创</option>
                <option selected value="2">转载</option>            
            '''
        ##########################################

        edit_bloginfo = {
            'bgcate' : bgcate_html,
            'ifcomment':ifcomment_html,
            'yuanchuang':yuanchuang_html,
            'ifyuanchuang':editblog_obj.yuanchuang,
            'userid':editblog_obj.uid.userid,
            'zlid':zlid_html,
            'title':editblog_obj.title,
            'label':editblog_obj.label,
            'ginfo':editblog_obj.ginfo,
            'beforeurl':editblog_obj.beforeurl,
        }
        return JsonResponse({'msg':1,'editinfo':edit_bloginfo})

#update_blog
def update_blog(request):
    if request.method == 'POST':
        blog_info = request.POST.dict()
        print(blog_info)
        if not all([blog_info['blogcate'], blog_info['blog_format'], blog_info['bloglx'], blog_info['user_id'],
                    blog_info['blog_flzl'], blog_info['blog_title'], blog_info['blog_bq'], blog_info['blog_content']]):
            return JsonResponse({'msg':0,'errormsg':'信息填写不完整！'})
        edituser_obj = models.Blog.objects.get(id=blog_info['edit_id'])
        uid_obj = models.Users.objects.get(userid=blog_info['user_id'])
        bgcate_obj = models.Blogcates.objects.get(id=blog_info['blogcate'])
        zlid_obj = models.Zhuanlan.objects.get(id=blog_info['blog_flzl'])
        if not edituser_obj:
            return JsonResponse({'msg':0,'errormsg':'没有这个用户！'})
        try:
            edituser_obj = models.Blog.objects.filter(id=blog_info['edit_id'])
            edituser_obj.update(
                title=blog_info['blog_title'],
                label=blog_info['blog_bq'],
                ginfo=blog_info['blog_content'],
                uid=uid_obj,
                bgcate=bgcate_obj,
                zlid=zlid_obj,
                ifcomment=int(blog_info['blog_format']) - 1,
                yuanchuang=int(blog_info['bloglx']) - 1,
                beforeurl=blog_info['before_url'],
                source='admin'
            )
            # 静态更新数据处理  title  blogcate blog_bq username bloglx blog_format
            if int(blog_info['bloglx']) -1 == 0:
                bloglx = '原创'
            else:
                bloglx = '转载'

            if int(blog_info['blog_format']) - 1 == 0:
                ifcomment_html = '''
                           <option selected value="0">公开</option>
                           <option value="1">私密</option>
                           <option value="2">公开但禁止评论</option>
                       '''
            elif int(blog_info['blog_format']) - 1 == 1:
                ifcomment_html = '''
                           <option value="0">公开</option>
                           <option selected value="1">私密</option>
                           <option value="2">公开但禁止评论</option>
                       '''
            else:
                ifcomment_html = '''
                           <option value="0">公开</option>
                           <option value="1">私密</option>
                           <option selected value="2">公开但禁止评论</option>
                           '''
            updateinfo = {
                'blogcate':bgcate_obj.title,
                'username':uid_obj.username,
                'bloglx':bloglx,
                'blog_format':ifcomment_html

            }
            return JsonResponse({'msg':1,'updateinfo':updateinfo})
        except Exception as e:
            print(str(e))
            return JsonResponse({'msg':0,'errormsg':'编辑失败，请联系管理员处理！'})

#发布状态更新
def uptateblog_ifcomment(request):
    if request.method =='POST':
        ifcomment_id = request.POST.get('ifcomment_id')
        ifcomment = request.POST.get('ifcomment')
        try:
            changeifcomment_obj = models.Blog.objects.get(id=ifcomment_id)
            changeifcomment_obj.ifcomment = int(ifcomment)
            changeifcomment_obj.save(force_update=True)
            return JsonResponse({'msg':1})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':0})

#逻辑删除
def delthis(request):
    if request.method == 'POST':
        i_id = request.POST.get('i_id','')
        status = request.POST.get('status','')
        try:
            del_obj = models.Blog.objects.get(id=i_id)
            del_obj.status = status
            del_obj.save(force_update=True)
            return JsonResponse({'msg':1,'successmsg':'博客状态已修改！'})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'修改失败！'})


#checkuserid
def checkuserid(request):
    if request.method == 'GET':
        userid = request.GET.get('username','')
        if not userid:
            return JsonResponse({'msg':0})
        checkuserid_obj = models.Users.objects.filter(userid=userid)
        if checkuserid_obj:
            blog_zl = models.Zhuanlan.objects.filter(uid=checkuserid_obj.first().id)
            #拼接分类专栏下拉框
            select_option=''
            for el in blog_zl:
                select_option+='''
                    <option value="{id}">{title}</option>
                '''.format(id=el.id,title=el.title)
            return JsonResponse({'msg':1,'select_option':select_option})
        else:
            return JsonResponse({'msg':0})
    else:
        return render(request,'404.html')

#markdown oss上传图片和缩略图处理
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def uploadimg(request):
    if request.method == "POST":
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