from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from apps.index import models
from w3lib.html import remove_tags
from django.db.models import Q
import markdown


# Create your views here.
# return render(request,'index.html',{'blogcate':blogcate_obj})

#尝试获取 登录用户的 ip
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def show(request):
    if request.method == 'GET':
        ip = get_client_ip(request)
        print(ip)
        try:
            new_ip = models.LoginLog(ip=ip)
            new_ip.save(force_insert=True)
        except Exception as e:
            print(e)

        blogcate_obj = models.Blogcates.objects.filter(status=0).order_by('-list_order')
        get_blog = int(request.GET.get('get_blog',0))
        bg_path = request.GET.get('path','')
        if get_blog == 0:
            if bg_path:
                bloginfo = models.Blog.objects.filter(status=0,ifcomment__in = [0,2],bgcate=models.Blogcates.objects.get(path=bg_path)).order_by('addtime')[:15]
            else:
                bloginfo = ''

            if not bloginfo:
                bloginfo = models.Blog.objects.filter(status=0,ifcomment__in=[0, 2]).order_by('-addtime')[:15]

            for pre_blog in bloginfo:
                if pre_blog.source == 'admin' or pre_blog.source == 'home':
                    pre_blog.ginfo = markdown.markdown(pre_blog.ginfo, extensions=[
                        'markdown.extensions.extra',
                        'markdown.extensions.codehilite',
                        'markdown.extensions.toc',
                    ])
                pre_blog.ginfo = remove_tags(pre_blog.ginfo)[:100]
            #  轮播图
            bannerinfo = models.Banner.objects.filter(status=1).order_by('pic_index')

            # 今日推荐
            today_top = models.Blog.objects.filter(status=0,ifcomment__in=[0, 2],).order_by('-today_looks')[:15]

            return render(request, 'index.html', {'blogcate': blogcate_obj,'bloginfo':bloginfo,'bannerinfo':bannerinfo,'today_top':today_top})
        # 不为 0 则是 ajax请求
        else:
            if bg_path:
                bloginfo = models.Blog.objects.filter(status=0,ifcomment__in=[0, 2],bgcate=models.Blogcates.objects.get(path=bg_path)).order_by('addtime')
            else:
                bloginfo = ''

            if not bloginfo:
                bloginfo = models.Blog.objects.filter(status=0,ifcomment__in=[0, 2],).order_by('-addtime')

            bloginfo_num = bloginfo.count()
            print(bloginfo_num)
            if get_blog*15 < bloginfo_num:
                bloginfo = bloginfo[get_blog*15:get_blog*15+15]
            else:
                return JsonResponse({'msg':'没有更多了！'})
            for pre_blog in bloginfo:
                pre_blog.ginfo = remove_tags(pre_blog.ginfo)[:100]
            bloginfo_html = ''
            for pre in bloginfo:
                bloginfo_html+='''
                    <li class="clearfix">
                            <div class="list_con">
                                <div class="title">
                                    <h2>
                                <a href="/user_{userid}/blog_{blogid}" >{blogtitle}</a>
                                </h2>
                                <div class="summary oneline">作者 | {auth} | {ginfo}…<div class="."></div>.</div>
                                <dl class="list_userbar">
                                 <dt>
                                <a href="/user_{userid}" target="_blank" class="user_img">
                                <img src="{head_url}" ">
                            </a>
                             </dt>
                                    <dd class="name">
                                        <a href="javascript:;" target="_blank">{auth}</a>
                                    </dd>
                                    <div class="interactive floatR">
                                        <!--阅读 begin-->
                                        <dd class="read_num">
                                            <a href="/user_{userid}/blog_{blogid}" >
                                                <span class="text">
                                                     <img src="https://jiamengweb.oss-cn-beijing.aliyuncs.com/hot.png" alt="" style="margin-top: -2px">
                                                </span>
                                                <span class="num">{look}</span>
                                            </a>
                                        </dd>
                                        <!--新增评论数+阅读 end-->
                                    </div>
                                </dl>
                                </div>
                            </div>
                        </li>
                '''.format(userid=pre.uid.userid,blogid=pre.id,auth=pre.uid.username,look=pre.look,ginfo=pre.ginfo,blogtitle=pre.title,head_url=pre.uid.head_url)
            return JsonResponse({'msg': 1, 'bloginfo_html': bloginfo_html})

from itertools import chain
def search(request):
    if request.method == 'GET':
        search_str = request.GET.get('search','')
        search_get_blog = int(request.GET.get('get_blog',0))
        bloginfo_1 = models.Blog.objects.filter(
            Q(status=0) &
            Q(ifcomment__in=[0,2]) &
            Q(title__contains=search_str)
        ).order_by('-look')[:10]
        bloginfo_2 = models.Blog.objects.filter(
            status=0,
            ifcomment__in=[0,2],
            uid__in=list(models.Users.objects.filter(username__contains=search_str))
        ).order_by('-look')
        bloginfo_2_userid = models.Blog.objects.filter(
            status=0,
            ifcomment__in=[0, 2],
            uid__in=list(models.Users.objects.filter(userid=search_str))
        ).order_by('-look')
        bloginfo_3 = models.Blog.objects.filter(
            Q(status=0) &
            Q(ifcomment__in=[0, 2]) &
            Q(title__contains=search_str) |
            Q(label__contains=search_str) |
            Q(ginfo__contains=search_str)
        ).order_by('-look')
        bloginfo = list(chain(bloginfo_1 , bloginfo_2 , bloginfo_3,bloginfo_2_userid))
        bloginfo_num = len(list(bloginfo))
        # 若不为0 说明是ajax在请求数据
        if search_get_blog != 0:
            if search_get_blog*15 < bloginfo_num:
                # 请求页数*15 ---> 请求页数*15+15
                bloginfo = bloginfo[search_get_blog*15:search_get_blog*15+15]
            else:
                return JsonResponse({'msg':'没有更多了！'})
            bloginfo_html =''
            for pre_blog in bloginfo:
                if pre_blog.source == 'admin' or pre_blog.source == 'home':
                    pre_blog.ginfo = markdown.markdown(pre_blog.ginfo, extensions=[
                        'markdown.extensions.extra',
                        'markdown.extensions.codehilite',
                        'markdown.extensions.toc',
                    ])
                pre_blog.ginfo = remove_tags(pre_blog.ginfo)[:100]
            for pre in bloginfo:
                bloginfo_html+='''
                    <li class="clearfix" >
                        <div class="list_con">
                            <h2>
                                <a href="/user_{userid}/blog_{blogid}" style="color: black;" >{blogtitle}</a>
                            </h2>
                            <div class="summary oneline">作者 | {auth} | {ginfo}…<div class="."></div></div>
                            <div class="name">
                                <a href="javascript:;" target="_blank">{auth}</a>
                            </div>
                            <div class="interactive floatR">
                                <!--阅读 begin-->
                                <dd class="read_num">
                                    <a href="/user_{userid}/blog_{blogid}" >
                                    <span class="text">
                                        <i class="layui-icon layui-icon-fire"></i>
                                    </span>
                                        <span class="num">{look}</span>
                                    </a>
                                </dd>
                            </div>
                        </div>
                    </li>
                '''.format(userid=pre.uid.id,blogid=pre.id,auth=pre.uid.username,look=pre.look,ginfo=pre.ginfo,blogtitle=pre.title)
            return JsonResponse({'msg':1,'bloginfo_html':bloginfo_html})

        bloginfo = bloginfo[:15]
        for pre_blog in bloginfo:
            if pre_blog.source == 'admin' or pre_blog.source == 'home':
                pre_blog.ginfo = markdown.markdown(pre_blog.ginfo, extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.toc',
                ])
            pre_blog.ginfo = remove_tags(pre_blog.ginfo)[:100]

        return render(request,'searchinfo.html',{'bloginfo':bloginfo,'search_str':search_str})

def pnf(request):
    return render(request,'404.html')
