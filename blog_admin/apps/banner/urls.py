# - * - coding:utf-8 - * -
from django.urls import path,re_path
from . import views
urlpatterns = [
    re_path(r'^$',views.show,name='banner_show'),
    #轮播图新增列表
    re_path(r'^inputbannerlist/$',views.inputbannerlist,name='inputbannerlist'),
    #up轮播图删除
    re_path(r'^delbanner/$',views.delbanner,name='delbanner'),
    #down轮播图删除
    re_path(r'^deldownbanner/$',views.deldownbanner,name='deldownbanner'),
    #启用--更新
    re_path(r'^updatabanner/$',views.updatabanner,name='updatabanner'),
    #check blogurl
    re_path(r'^checkurl/$',views.checkurl,name='checkurl'),
    #启用按钮获取该图片详细信息
    re_path(r'^getblogdetail/$',views.getblogdetail,name='getblogdetail'),
    # update_up_banner
    re_path(r'^update_up_banner/$',views.update_up_banner,name='update_up_banner')

]