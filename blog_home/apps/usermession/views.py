from django.shortcuts import render
from django.http import JsonResponse
from apps.index import models
from w3lib.html import remove_tags
import markdown
from django.db.models import Q
# Create your views here.


def show(request,uid):
    if request.method == 'GET':
        search_get_blog = int(request.GET.get('get_blog',0))
        userinfo =models.Users.objects.get(userid=uid)
        bloginfo = models.Blog.objects.filter(status=0,uid=userinfo)
        bloginfo_num = bloginfo.count()
        if bloginfo_num == 0:
            return render(request,'usermession.html',{'userinfo':userinfo,'bloginfo': 0})
        # 若不为0 说明是ajax在请求数据
        if search_get_blog != 0:
            if search_get_blog * 15 < bloginfo_num:
                # 请求页数*15 ---> 请求页数*15+15
                bloginfo = bloginfo[search_get_blog * 15:search_get_blog * 15 + 15]
            else:
                return JsonResponse({'msg': '没有更多了！'})
            bloginfo_html = ''
            for pre_blog in bloginfo:
                pre_blog.ginfo = remove_tags(pre_blog.ginfo)[:100]
            for pre in bloginfo:
                bloginfo_html += '''
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
                       '''.format(userid=pre.uid.id, blogid=pre.id, auth=pre.uid.username, look=pre.look,
                                  ginfo=pre.ginfo, blogtitle=pre.title)
            return JsonResponse({'msg': 1, 'bloginfo_html': bloginfo_html})

        bloginfo = bloginfo[:15]
        for pre_blog in bloginfo:
            if pre_blog.source == 'admin' or pre_blog.source == 'home':
                pre_blog.ginfo = markdown.markdown(pre_blog.ginfo, extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.toc',
                ])
            pre_blog.ginfo = remove_tags(pre_blog.ginfo)[:100]
        return render(request,'usermession.html',{'userinfo':userinfo,'bloginfo': bloginfo})




def lyban(request,uid):
    if request.method== 'POST':
        user_id = login_or_msg(request)
        reuser_id = request.POST.get('user_id','')
        if (not reuser_id) or int(user_id) != int(reuser_id):
            return JsonResponse({'msg':'登录失效'})
        lycont = request.POST.get('lycont','')
        try:
            user_obj = models.Users.objects.get(id=user_id)
            user_obj.yl_1 = lycont
            user_obj.save(force_update=True)
            return JsonResponse({'msg':1})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'更新失败！'})


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
