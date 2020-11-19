from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from apps.index import models
from django.core.paginator import Paginator
from w3lib.html import remove_tags
from django.db.models import Q
import markdown


# 闭包 检测当前用户是否登陆 跳转到登录页
def check_login_tologin(func):
    def inner(request, *args, **kwargs):
        # 获取session判断用户是否登陆
        if request.session.get('userinfo'):
            # 已经登录的用户...
            return func(request, *args, **kwargs)
        else:
            # 没有登录的用户，跳转刚到登录页面
            return redirect('/login')
    return inner

# 闭包 检测当前用户是否登陆 返回未登录json提示信息
def check_login_tomsg(func):
    def inner(request, *args, **kwargs):
        # 获取session判断用户是否登陆
        if request.session.get('userinfo'):
            # 已经登录的用户...
            return func(request, *args, **kwargs)
        else:
            # 没有登录的用户，跳转刚到登录页面
            return JsonResponse({'msg':'请先登录!'})
    return inner

@check_login_tologin
def show(request):
    if request.method == 'GET':
        user_id = login_or_404(request)
        userinfo = models.Users.objects.get(id=user_id)
        return render(request,'profile.html',{'userinfo':userinfo})
    elif request.method == 'POST':
        user_id =login_or_404(request)
        username = request.POST.get('username','')
        head_url = request.POST.get('head_url','')
        try:
            user_obj = models.Users.objects.get(id=user_id)
            user_obj.username =username
            user_obj.head_url =head_url
            user_obj.save(force_update=True)
            request.session["userinfo"] = {'username': user_obj.username, 'userimg': user_obj.head_url,
                                           'userid': user_obj.id}
            return redirect('/userprofile')
        except Exception as e:
            print(e)
            return redirect('/userprofile')


@check_login_tologin
def collection_list(request):
    if request.method == 'GET':
        user_id = login_or_404(request)
        user_obj = models.Users.objects.get(id=user_id)
        collection_obj = models.Collect.objects.filter(status=0,uid=user_obj)
        # 收藏列表分页
        p = int(request.GET.get('page',1))
        paginator = Paginator(collection_obj,5)
        collection_obj = paginator.page(p)
        total_pages = paginator.num_pages

        # 处理数据  添加 count 统计 collection.collent_blog的数量
        for pre in collection_obj:
            collect_num = len(split_model(pre.collect_blog,'list'))-1
            pre.count = collect_num


        return render(request,'mycollect.html',{'collection':collection_obj,'total_pages':total_pages})


# 新建收藏夹
@check_login_tomsg
def addcollection(request):
    if request.method == "POST":
        # 当前登陆的用户id
        user_id = login_or_msg(request)
        user_obj = models.Users.objects.get(id=user_id)
        flzl = request.POST.get('flzl','')
        if flzl == '':
            return JsonResponse({'msg':'收藏夹名称不能为空！'})
        check_cname = models.Collect.objects.filter(status=0,uid=user_obj,title=flzl).count()
        if check_cname:
            return JsonResponse({'msg':'该收藏夹已存在！'})
        try:
            collection_obj = models.Collect(
                title = flzl,
                uid = user_obj,
            )
            collection_obj.save(force_insert=True)
            return JsonResponse({'msg':1})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'添加失败！'})

# 新建 专栏
@check_login_tomsg
def addflzl(request):
    if request.method == "POST":
        # 当前登陆的用户id
        user_id = login_or_msg(request)
        user_obj = models.Users.objects.get(id=user_id)
        flzl = request.POST.get('flzl','')
        if flzl == '':
            return JsonResponse({'msg':'专栏名称不能为空！'})
        check_cname = models.Zhuanlan.objects.filter(status=0,uid=user_obj,title=flzl).count()
        if check_cname:
            return JsonResponse({'msg':'该专栏已存在！'})
        try:
            collection_obj = models.Zhuanlan(
                title = flzl,
                uid = user_obj,
            )
            collection_obj.save(force_insert=True)
            return JsonResponse({'msg':1})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'添加失败！'})


# 查看收藏博客
@check_login_tomsg
def col_list(request,cid):
    if request.method == 'GET':
        user_id = login_or_404(request)
        user_obj = models.Users.objects.get(id=user_id)
        collention_obj = models.Collect.objects.filter(status=0,id=cid)
        colbg_list = split_model(collention_obj[0].collect_blog,'list')
        bgls = []
        for pre in colbg_list:
            if pre != '0':
                try:
                    bg_obj = models.Blog.objects.filter(status=0,id=pre).first()
                    if bg_obj.source == 'admin' or bg_obj.source == 'home':
                        bg_obj.ginfo = markdown.markdown(bg_obj.ginfo, extensions=[
                            'markdown.extensions.extra',
                            'markdown.extensions.codehilite',
                            'markdown.extensions.toc',
                        ])
                    bg_obj.ginfo = remove_tags(bg_obj.ginfo)[:50] + '...'
                    bgls.append(bg_obj)
                except:
                    continue
        p = int(request.GET.get('page',1))
        paginator = Paginator(bgls,5)
        bgls = paginator.page(p)
        total_pages = paginator.num_pages



        return render(request,'col_list.html',{'bgls':bgls,'total_pages':total_pages})

# 查看专栏博客
@check_login_tomsg
def bg_list(request,cid):
    if request.method == 'GET':
        user_id = login_or_404(request)
        user_obj = models.Users.objects.get(id=user_id)
        # 检查权限
        zl_obj = models.Zhuanlan.objects.filter(id=cid,status=0,uid=user_obj)
        if not zl_obj.count() :
            return render(request,'404.html')
        else:
            zl_obj = zl_obj.first()
        # 取出专栏下的博客
        collention_obj = models.Blog.objects.filter(status=0,zlid=zl_obj,uid=user_obj)

        for pre in collention_obj:
            try:
                if pre.source == 'admin' or pre.source == 'home':
                    pre.ginfo = markdown.markdown(pre.ginfo, extensions=[
                        'markdown.extensions.extra',
                        'markdown.extensions.codehilite',
                        'markdown.extensions.toc',
                    ])
                pre.ginfo = remove_tags(pre.ginfo)[:50] + '...'
            except:
                continue

        p = int(request.GET.get('page',1))
        paginator = Paginator(collention_obj,5)
        collention_obj = paginator.page(p)
        total_pages = paginator.num_pages

        # 当前登录用户的全部专栏
        user_zl = models.Zhuanlan.objects.filter(status=0,uid=user_obj)

        return render(request,'bg_list.html',{'collention_obj':collention_obj,'total_pages':total_pages,'user_zl':user_zl})

# 删除收藏夹
@check_login_tomsg
def delcol(request):
    if request.method == 'POST':
        user_id = login_or_msg(request)
        del_id = request.POST.get('delid','')
        if del_id == '':
            return JsonResponse({'msg':'请稍后再试！'})
        try:
            user_obj = models.Users.objects.get(id=user_id)
            del_obj = models.Collect.objects.filter(status=0,uid=user_obj,id=del_id)
            if not del_obj.count() :
                return JsonResponse({'msg':'登陆失效！'})
            del_obj = del_obj.first()
            del_obj.status = 1
            del_obj.save(force_update=True)
            return JsonResponse({'msg':1})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'删除失败！'})

# 删除专栏
@check_login_tomsg
def delzl(request):
    if request.method == 'POST':
        user_id = login_or_msg(request)
        del_id = request.POST.get('delid','')
        if del_id == '':
            return JsonResponse({'msg':'请稍后再试！'})
        try:
            user_obj = models.Users.objects.get(id=user_id)
            del_obj = models.Zhuanlan.objects.filter(status=0,uid=user_obj,id=del_id)
            if not del_obj.count() :
                return JsonResponse({'msg':'登陆失效！'})

            # 首先删除当前专栏  ---> 过滤所有zlid == 当前专栏的博客 将其 zlid 全部指向 --->（该用户专栏中title == 默认专栏）
            del_obj = del_obj.first()
            # 防止恶意访问 判断所删除专栏是否为默认
            if del_obj.title == '默认专栏':
                return JsonResponse({'msg': '默认专栏不可删除！'})
            del_obj.status = 1
            del_obj.save(force_update=True)
            change_bg = models.Blog.objects.filter(status=0,uid=user_obj,zlid=del_obj)
            if not change_bg:
                # 说明删了一个空白专栏 直接返回结果
                return JsonResponse({'msg':1})
            else:
                # 说明删除的专栏非空
                # 过滤出当前登陆user下所有 zlid == change_bg.id 的博客 将其 zlid全部update 为当前登录用户zhuanlan表下title == 默认专栏的 id
                user_get_default_zlid = models.Zhuanlan.objects.filter(uid=user_obj,title='默认专栏').first().id
                user_default_zl_obj = models.Zhuanlan.objects.get(id=user_get_default_zlid)
                for pre in change_bg:
                    pre.zlid=user_default_zl_obj
                    pre.save(force_update=True)
                return JsonResponse({'msg':1})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'删除失败！'})

#删除博客
@check_login_tomsg
def del_bg(request,cid):
    if request.method == 'POST':
        user_id = login_or_msg(request)
        del_id = request.POST.get('delid','')
        if del_id == '':
            return JsonResponse({'msg':'请稍后再试！'})
        try:
            user_obj = models.Users.objects.get(id=user_id)
            del_obj = models.Blog.objects.filter(status=0,uid=user_obj,id=del_id)
            if not del_obj.count() :
                return JsonResponse({'msg':'登陆失效！'})
            del_obj = del_obj.first()
            del_obj.status=1
            del_obj.save(force_update=True)
            return JsonResponse({'msg':1})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'删除失败！'})

# 移动博客
@check_login_tomsg
def move_bg(request,cid):
    if request.method == 'POST':
        user_id = login_or_msg(request)
        user_obj = models.Users.objects.get(id=user_id)
        move_id =str(request.POST.get('move_id',''))
        move_zl_id =str(request.POST.get('move_zl_id',''))
        if move_id == '':
            return JsonResponse({'请稍后重试！'})
        if move_zl_id == str(cid):
            return JsonResponse({'msg':'已经在当前专栏了！'})
        check_blog = models.Blog.objects.filter(status=0,uid=user_obj,zlid=cid,id=move_id)
        if not check_blog.count():
            return JsonResponse({'登陆失效！'})
        check_blog = check_blog.first()
        check_blog.zlid = models.Zhuanlan.objects.get(id=move_zl_id)
        check_blog.save(force_update=True)
        return JsonResponse({'msg':1})



@check_login_tomsg
def cancel_col(request,cid):
    if request.method == 'POST':
        user_id = login_or_msg(request)
        del_id = request.POST.get('delid','')
        if del_id == '':
            return JsonResponse({'msg':'请稍后再试！'})
        try:
            user_obj = models.Users.objects.get(id=user_id)
            del_obj = models.Collect.objects.filter(status=0,uid=user_obj,id=cid)
            if not del_obj.count() :
                return JsonResponse({'msg':'登陆失效！'})
            del_obj = del_obj.first()
            del_obj_list = split_model(del_obj.collect_blog,'list')
            del_obj_list.remove(str(del_id))
            del_obj_str = split_model(del_obj_list,'str')
            del_obj.collect_blog = del_obj_str
            del_obj.save(force_update=True)
            return JsonResponse({'msg':1})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'删除失败！'})

# 博客管理 首页
@check_login_tologin
def myblog(request):
    if request.method == 'GET':
        user_id = login_or_404(request)
        user_obj = models.Users.objects.get(id=user_id)
        user_flzl = models.Zhuanlan.objects.filter(status=0,uid=user_obj)

        # 分页
        p = int(request.GET.get('page',1))
        paginator = Paginator(user_flzl,5)
        user_flzl = paginator.page(p)
        total_pages = paginator.num_pages
        # 统计专栏下的博客数量
        for pre in user_flzl:
            pre.count = models.Blog.objects.filter(status=0,zlid=pre).count()

        return render(request,'myblog.html',{
            'user_flzl':user_flzl,
            'total_pages':total_pages
        })

# 评论管理页面
@check_login_tologin
def mycomment(request):
    if request.method == 'GET':
        user_id = login_or_404(request)
        user_obj = models.Users.objects.get(id=user_id)
        comment_type = int(request.GET.get('comment_type','100'))
        if comment_type == 1:
            # 我评论的博客
            comment_obj_first = models.Comment.objects.filter(status=0, uid=user_obj)
            # 回复我评论的评论
            comment_list = []
            for pre in comment_obj_first:
                comment_list.extend(list(models.Comment.objects.filter(status=0, parentid=pre.id)))
            comment_list.extend(list(comment_obj_first))
            print(comment_list)

            comment_obj = bubble_sort(list(set(comment_list)))
            print(comment_obj)

            p = int(request.GET.get('page', 1))
            paginator = Paginator(comment_obj, 6)
            comment_obj = paginator.page(p)
            total_pages_1 = paginator.num_pages

            for pre in comment_obj:
                if len(pre.ginfo) > 59:
                    pre.ginfo = pre.ginfo[:59] + '...'
                else:
                    pass

            return render(request,'mycomment_2.html',{'comment_obj':comment_obj,'total_pages_1':total_pages_1})

        else:
            user_blog_all = models.Blog.objects.filter(status=0, uid=user_obj)
            comment_list = []
            for pre_blog in user_blog_all:
                comment_list.extend(list(models.Comment.objects.filter(status=0, bid=pre_blog, parentid=0)))

            comment_list = MergeSort(comment_list)
            p = int(request.GET.get('page', 1))
            paginator_s = Paginator(comment_list, 6)
            comment_list = paginator_s.page(p)
            total_pages_0 = paginator_s.num_pages

            for pre in comment_list:
                if len(pre.ginfo) > 59:
                    pre.ginfo = pre.ginfo[:59] + '...'
                else:
                    pass

            return render(request,'mycomment.html',{'comment_list':comment_list,'total_pages_0':total_pages_0})


#删除评论
@check_login_tologin
def co_del(request):
    if request.method== 'POST':
        del_col_id = request.POST.get('del_col_id','')
        if not del_col_id:
            return JsonResponse({'网络繁忙，请稍后重试！'})
        try:
            com_obj = models.Comment.objects.get(id=del_col_id)
            com_obj.status=1
            com_obj.save(force_update=True)
            try:
                if com_obj.parentid == 0:
                    com_obj_sec = models.Comment.objects.filter(parentid=com_obj.id)
                    for pre in com_obj_sec:
                        pre.status=1
                        pre.save(force_update=True)
            except Exception as e:
                print(e)
                pass
            return JsonResponse({'msg':1})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'删除失败'})

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

import datetime,time

def date_to_timenum(date):
    date_str = str(date)

    # 先把date转变为字符串,然后转换为datetime格式
    try:
        this_date = datetime.datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S')

        # 把datetime转变为时间戳
        this_date = time.mktime(this_date.timetuple())

        return this_date
    except:
        this_date = datetime.datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S.%f')

        # 把datetime转变为时间戳
        this_date = time.mktime(this_date.timetuple())*1000+this_date.microsecond / 1000.0

        return this_date

# 冒泡排序
def bubble_sort(array):
    n = len(array)
# 一共需要n-1次循环，每一个数都需要找到没拍好序的最大值
    for i in range(n-1):
# 将没有拍好序的数组找到最大值，并一直讲最大值换到最顶端
        for j in range(n-i-1):
# 依次比较，将两者较大的往后放
            if date_to_timenum(array[j].addtime) < date_to_timenum(array[j+1].addtime):
                array[j], array[j+1] = array[j+1], array[j]
    return array

# 归并排序
def MergeSort(arrayList):
    arrayListLen = len(arrayList)
    # 如果长度小于等于1，就返回array即可
    if arrayListLen <= 1:
        return arrayList
    # 取中间值
    middleNum = arrayListLen >> 1
    # 左边的部分去做MergeSort
    leftArray = MergeSort(arrayList[:middleNum])
    # 右边的部分去做MergeSort
    rightArray = MergeSort(arrayList[middleNum:])
    # 将左右两边合并，成为一个新的数组，并已经排序成功
    return MergeCore(leftArray, rightArray)
def MergeCore(leftArray, rightArray):
    # 首先需要定义两个指针，这两个指针分别指向两个数组的第一个元素
    leftPointer, rightPointer = 0, 0
    # 定义一个返回列表(这一步就代表控件复杂度至少是O(n))
    retArray = []
    # 循环两个数组，循环最小值加入到返回值得数组中
    while leftPointer < len(leftArray) and rightPointer < len(leftArray):
        if date_to_timenum(leftArray[leftPointer].addtime) > date_to_timenum(rightArray[rightPointer].addtime):
            retArray.append(leftArray[leftPointer])
            leftPointer += 1
        else:
            retArray.append(rightArray[rightPointer])
            rightPointer += 1
    # 下面的代码是将剩余的数组中的内容放置到返回的数组中
    retArray += leftArray[leftPointer:]
    retArray += rightArray[rightPointer:]
    # retList.extend(leftArray[leftPointer:])
    # retList.extend(rightArray[rightPointer:])
    return retArray