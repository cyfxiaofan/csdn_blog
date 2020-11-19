from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from apps.index import models
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

class Show(View):
    def get(self,request):
        keywords = request.GET.get('keywords','')
        if keywords:
            search_obj = models.Blogcates.objects.filter(
                Q(id__contains=keywords) |
                Q(title__icontains=keywords) |
                Q(path__icontains=keywords) |
                Q(list_order__contains=keywords)
            ).order_by('-list_order')
        else:
            search_obj = models.Blogcates.objects.all().order_by('-list_order')
        if not search_obj:
            search_obj = models.Blogcates.objects.all().order_by('-list_order')

        p = Paginator(search_obj,10)
        page = int(request.GET.get('page',1))
        totalpages = p.num_pages
        rankpagelist = p.page(page)
        return render(request,'blogcate/blogcate.html',{'all_result':rankpagelist,'totalpages':totalpages,'keywords':keywords})



class Addblogcate(View):
    def get(self,request):
        return render(request,'blogcate/addblogcate.html')
    def post(self,request):
        blogcatetitle = request.POST.get('blogcatetitle','')
        path = request.POST.get('path','')
        checktitle = models.Blogcates.objects.filter(title=blogcatetitle)
        checkpath = models.Blogcates.objects.filter(path=path)
        if (checktitle and checkpath):
            return render(request, 'blogcate/addblogcate.html', {
                # 'current_category': {'name': blogcatetitle, 'path': path},
                'jscode': "swal('该路由已存在！','请重试！','error')",
            })

        orderpoint = request.POST.get('orderpoint','')
        if not all([blogcatetitle,path,orderpoint]):
            return render(request,'blogcate/addblogcate.html',{
                # 'current_category':{'name':blogcatetitle,'path':path,'list_order':orderpoint},
                'jscode':"swal('信息填写不完整！','请完善信息再提交！','error')",
            })
        try:
            addobj = models.Blogcates(
                title=blogcatetitle,
                path=path,
                list_order=orderpoint
            )
            addobj.save(force_insert=True)
            return render(request,'blogcate/addblogcate.html',{'jscode':"swal('添加成功！','博客分类信息已添加！','success')"})
        except Exception as e:
            print(str(e))
            return render(request, 'blogcate/addblogcate.html', {
                # 'current_category': {'name': blogcatetitle, 'path': path, 'list_order': orderpoint},
                'jscode': "swal('添加失败！','请联系管理员处理！','error')",
            })

class Editblogcate(View):
    def post(self,request):
        msg = request.POST.dict()
        # 拿到要修改的对像
        checkchange = models.Blogcates.objects.get(id=msg['lid'])
        # 检查更新数据的合法性
        if msg['lname'] != checkchange.title :
            checktitle = models.Blogcates.objects.filter(title=msg['lname']).count()
            if checktitle :
                return JsonResponse({'msg':'博客分类名称重复!'})
        if msg['lpath'] != checkchange.path :
            checkpath = models.Blogcates.objects.filter(path=msg['lpath']).count()
            if checkpath:
                return JsonResponse({'msg': '博客分类路由重复!'})
        try:
            checkchange.title = msg['lname']
            checkchange.path = msg['lpath']
            checkchange.list_order = msg['lorder']
            checkchange.save(force_update=True)
            return JsonResponse({'msg':'修改成功'})
        except Exception as e:
            print(str(e))
            return JsonResponse({'msg':'修改失败，请重试或联系管理员处理！'})

class Delthis(View):
    def post(self,request):
        i_id = request.POST.get('i_id', '')
        status = request.POST.get('status', '')
        try:
            del_obj = models.Blogcates.objects.get(id=i_id)
            del_obj.status = status
            del_obj.save(force_update=True)
            return JsonResponse({'msg': 1, 'successmsg': '博客路由状态已修改！'})
        except Exception as e:
            print(e)
            return JsonResponse({'msg': '修改失败！'})



class Checkblogcatename(View):
    def get(self,request):
        blogname = request.GET.get('blogname','')
        checkobj = models.Blogcates.objects.filter(title=blogname).count()
        if checkobj:
            return JsonResponse({'msg':0})
        return JsonResponse({'msg':1})
    def post(self,request):
        return render(request,'404.html')

class Checkblogcatepath(View):
    def get(self,request):
        blogpath = request.GET.get('blogpath','')
        checkobj = models.Blogcates.objects.filter(path=blogpath).count()
        if checkobj:
            return JsonResponse({'msg':0})
        return JsonResponse({'msg':1})
