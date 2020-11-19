# - * - coding:utf-8 - * -
from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.show,name='blog_show'),
    re_path(r'^addblog/$', views.addblog,name='blog_add'),
    #上传图片、
    re_path(r'^uploadimg/$',views.uploadimg,name='uploadimg'),
    #checkuserid
    re_path(r'^checkuserid/$',views.checkuserid,name='checkuserid'),
    #获取编辑博客信息
    re_path(r"^edit_blog/$",views.edit_blog,name='edit_blog'),
    #更新编辑信息
    re_path(r'^update_blog/$',views.update_blog,name='update_blog'),
    #发布状态更新
    re_path(r'^uptateblog_ifcomment/$',views.uptateblog_ifcomment,name='uptateblog_ifcomment'),
    #逻辑删除
    re_path(r'^delthis/$',views.delthis,name='delthis')
]