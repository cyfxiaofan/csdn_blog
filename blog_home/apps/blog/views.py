from django.shortcuts import render,redirect
from apps.index import models
import markdown
from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse
from django.db.models import Q
from w3lib.html import remove_tags
# Create your views here.

# 检查博客的评论权限
def checkblogcomment_msg(func):
    def inner(request,uid,bid):
        # 是 POST 说明是在发表评论
        if request.method == 'POST':
            co_obj = models.Blog.objects.get(id=bid)
            if co_obj.ifcomment != 2:
                return func(request,uid,bid)
            else:
                return HttpResponse("<script>alert('本文章禁止评论!');history.back(-1)</script>")
        else:
            return func(request, uid, bid)
    return inner


@checkblogcomment_msg
def show(request,uid,bid):
    if request.method == 'GET':
        print(uid,bid)
        user_obj = models.Users.objects.filter(userid=uid,status=0)
        if not user_obj:
            return render(request,'404.html')
        bloginfo = models.Blog.objects.filter(id = bid,status=0,ifcomment__in=[0,2])
        if not bloginfo:
            return render(request,'404.html')
        if (int(bloginfo[0].uid.userid) != int(uid)) or (bloginfo[0].status == 1):
            return render(request,'404.html')
        bloginfo = bloginfo[0]
        bloginfo.look = int(bloginfo.look)+1
        bloginfo.save(force_update=True)
        if bloginfo.yuanchuang == 0:
            bloginfo.yuanchuang = '原创'
        else:
            bloginfo.yuanchuang = '转载'
        if bloginfo.source == 'admin' or bloginfo.source == 'home':
            bloginfo.ginfo = markdown.markdown(bloginfo.ginfo,extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ])

        # 评论接口数据处理
        # 接口数据 {
        #   first_comment_1:[second_obj_1_1,second_obj_1_2],
        #   first_comment_2:[second_obj_2_1,second_obj_2_2],
        #   ...
        # }

        commentinfos = models.Comment.objects.filter(status=0,bid=models.Blog.objects.get(id=bid)).filter(parentid=0).order_by('-affirm')


        # 对一级评论数据分页
        p = int(request.GET.get('page',1))
        paginator = Paginator(commentinfos,'10')
        commentinfo = paginator.page(p)
        totalpages = paginator.num_pages

       #获取对当前博客的所有的论评
        commentinfos_all = models.Comment.objects.filter(status=0,bid=models.Blog.objects.get(id=bid))

        #判断当前登陆user的点赞 并且为当前登陆user 添加浏览历史，
        user_id = login_or_false(request)
        if user_id:
            user_obj_login = models.Users.objects.get(id=user_id)
            # 判断是否收藏
            if check_collect(user_obj_login,bid) :
                iscollect = 1
            else:
                iscollect = 0

            # 收藏夹数据
            zlid_obj = models.Collect.objects.filter(status=0,uid=user_obj_login)

            for pre_comment in commentinfos_all:
                check_list = pre_comment.affim_user.split('|')
                if str(user_id) in check_list :
                    pre_comment.is_affirm = 1
                else:
                    pre_comment.is_affirm = 0
            for pre_comment in commentinfo:
                check_list = pre_comment.affim_user.split('|')
                if str(user_id) in check_list :
                    pre_comment.is_affirm = 1
                else:
                    pre_comment.is_affirm = 0

            # 博客点赞
            check_affirm_blog_list = user_obj_login.affirm_blog.split('|')
            if str(bid) in check_affirm_blog_list:
                bloginfo.is_blog_affirm = 1
            else:
                bloginfo.is_blog_affirm = 0

            if user_obj_login.bghistory :
                user_obj_login.bghistory = user_obj_login.bghistory+'|'+str(bid)
            else:
                user_obj_login.bghistory = str(bid)
            user_obj_login.save(force_update=True)
        else:
            zlid_obj = ''
            iscollect = 0

        # 处理为接口数据
        commentinfo = dict(zip([first_comment for first_comment in commentinfo],
                                [[j for j in commentinfos_all if j.parentid == i.id] for i in commentinfo ]))

        # 分类专栏
        flzl = models.Zhuanlan.objects.filter(uid=user_obj[0],status=0)

        for per in flzl:
            blog_num = models.Blog.objects.filter(zlid=per,status=0).count()
            per.blog_num =blog_num

        # 热门分类
        remen_blog = models.Blog.objects.filter(status=0,uid=user_obj[0]).order_by('-look')[:10]

        # 15个推荐  结合当前博客的标题给出15个合理的搜索推荐
        blog_tuijian = models.Blog.objects.filter( Q(status=0) &(
                                                   Q(label__contains=bloginfo.title) |
                                                   Q(title__contains=bloginfo.title) |
                                                   Q(bgcate=models.Blogcates.objects.get(id=bloginfo.bgcate.id)) )
                                                  ).order_by('-affirm')[:17]

        for pre_blog in blog_tuijian:
            if pre_blog.source == 'admin' or pre_blog.source == 'home':
                pre_blog.ginfo = markdown.markdown(pre_blog.ginfo, extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.toc',
                ])
            pre_blog.ginfo = remove_tags(pre_blog.ginfo)[:100]
            pre_blog.title = pre_blog.title[:15]

        return render(request,'blog_detail.html',{'bloginfo':bloginfo,'commentinfo':commentinfo,'totalpages':totalpages,'flzl':flzl,'remen_blog':remen_blog,'blog_tuijian':blog_tuijian,'zlid_obj':zlid_obj,'iscollect':iscollect})
    elif request.method == 'POST':
        commentinfo = request.POST.dict()
        print(commentinfo)
        #{'csrfmiddlewaretoken': 'Chc4IHvGfyuf7mD07Wz8HfPHurBEhIHO9Vs84Xb9Pi67iDuZrxgHhctkkI1qdqlz',
        # 'comment_content': 'hellow',
        # 'article_id': '105',
        # 'comment_userId': '2',
        # 'parentid': '1',
        # 'applyid': '2'}
        try:
            user_id = login_or_404(request)
            apply_blog = models.Comment.objects.get(id=commentinfo['applyid'])
            reply_user = models.Users.objects.get(id=user_id)
            blog_obj = models.Blog.objects.get(id=commentinfo['article_id'])
            new_comment_obj = models.Comment(
                ginfo = commentinfo['comment_content'],
                parentid=commentinfo['parentid'],
                bid=blog_obj,
                uid=reply_user,
                applyid=apply_blog,
            )
            new_comment_obj.save(force_insert=True)
            try:
                reply_user.yl_2 = str(int(reply_user.yl_2) + 1)
            except:
                reply_user.yl_2 = str(0 + 1)
            reply_user.save(force_update=True)
            return redirect('/user_'+uid+'/blog_'+bid)
        except Exception as e:
            print(e)
            return redirect('/user_' + uid + '/blog_' + bid)


def comment_affirm(request,uid,bid):
    if request.method == 'GET':
        print(uid,bid)
        user_id = login_or_msg(request)
        comment_id = request.GET.get('comment_id','')
        if not comment_id:
            return JsonResponse({'msg':'网络繁忙，请稍后重试···'})
        try:
            comment_obj = models.Comment.objects.get(id=comment_id)
            checkcomment_list = comment_obj.affim_user.split('|')
            if str(user_id) in checkcomment_list:
                checkcomment_list.remove(str(user_id))
                checkcomment_str = '|'.join(checkcomment_list)
                comment_obj.affim_user=checkcomment_str
                comment_obj.affirm = int(comment_obj.affirm)-1
                comment_obj.save(force_update=True)
                return JsonResponse({'msg':'lose'})
            else:
                comment_obj.affirm = int(comment_obj.affirm)+1
                comment_obj.affim_user = comment_obj.affim_user+'|'+str(user_id)
                comment_obj.save(force_update=True)
            return JsonResponse({'msg':'add'})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'网络繁忙，请稍后重试···'})

def affirm_blog(request,uid,bid):
    if request.method == 'GET':
        user_id = request.GET.get('user_id','')
        user_id_login = login_or_msg(request)
        if str(user_id) != str(user_id_login):
            return JsonResponse({'msg':'登录失效，请重新登陆再试！'})
        try:
            user_obj= models.Users.objects.get(id=user_id)
            blog_obj = models.Blog.objects.get(id=bid)
            checkblog_list = user_obj.affirm_blog.split('|')

            if str(bid) in checkblog_list :
                checkblog_list.remove(str(bid))
                checkblog_str = '|'.join(checkblog_list)
                user_obj.affirm_blog = checkblog_str
                blog_obj.affirm = int(blog_obj.affirm) - 1
                blog_obj.save(force_update=True)
                try:
                    user_obj.yl_2 = str(int(user_obj.yl_2)-1)
                except:
                    user_obj.yl_2 = str(0 - 1)
                user_obj.save(force_update=True)
                return JsonResponse({'msg': 'lose'})
            else:
                user_obj.affirm_blog = user_obj.affirm_blog+'|'+str(bid)
                blog_obj.affirm = int(blog_obj.affirm) + 1
                blog_obj.save(force_update=True)
                try:
                    user_obj.yl_2 = str(int(user_obj.yl_2)+1)
                except:
                    user_obj.yl_2 = str(0 + 1)
                user_obj.save(force_update=True)
                return JsonResponse({'msg': 'add'})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'网络繁忙，请稍后重试···'})

def addcollection(request,uid,bid):
    if request.method == "POST":
        # 当前登陆的用户id
        user_id = login_or_msg(request)
        flzl = request.POST.get('flzl','')
        if flzl == '':
            return JsonResponse({'msg':'收藏夹名称不能为空！'})
        try:
            user_obj = models.Users.objects.get(id=user_id)
            collection_obj = models.Collect(
                title = flzl,
                uid = user_obj,
            )
            collection_obj.save(force_insert=True)
            zl_html = '''
                 <option value="{id}">{title}</option>' 
            '''.format(id=collection_obj.id,title=collection_obj.title)
            return JsonResponse({'msg':1,'zl_html':zl_html})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'添加失败！'})

def collectblog(request,uid,bid):
    if request.method == 'POST':
        user_id = login_or_msg(request)
        user_obj = models.Users.objects.get(id=user_id)
        scselector = request.POST.get('scselector','')
        if scselector == '':
            return JsonResponse({'msg':'收藏失败！请重试'})
        collect_obj = models.Collect.objects.get(id=scselector)
        collect_list = split_model(collect_obj.collect_blog,'list')
        if str(bid) in collect_list:
            return JsonResponse({'msg':'您已经收藏过了！'})
        else:
            collect_list.append(str(bid))
            collect_str = split_model(collect_list,'str')
        try:
            collect_obj.collect_blog = collect_str
            collect_obj.save(force_update=True)
            try:
                user_obj.yl_2 = str(int(user_obj.yl_2) + 1)
            except:
                user_obj.yl_2 = str(0 + 1)
            user_obj.save(force_update=True)
            return JsonResponse({'msg':1})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'收藏失败！'})


#判段当前博客是否被当前登录用户收藏
def check_collect(user_obj,bid):
    '''
    :param user_obj: user_obj
    :param bid: blogid
    :return: True or False
    '''
    collect_obj = models.Collect.objects.filter(status=0,uid=user_obj)
    for pre in collect_obj:
        collect_list = split_model(pre.collect_blog,'list')
        if str(bid) in collect_list:
            return True
    return False


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



# 验证当前是否登陆
def login_or_404(request):
    try:
        user_session = request.session.get('userinfo')
        user_id = user_session['userid']
        if not user_id:
            return render(request,'404.html')
        else:
            return user_id
    except:
        return render(request,'404.html')

# 验证当前是否登陆
def login_or_false(request):
    try:
        user_session = request.session.get('userinfo')
        user_id = user_session['userid']
        if not user_id:
            return False
        else:
            return user_id
    except Exception as e:
        return False




