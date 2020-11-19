# - * - coding:utf-8 - * -
from django.urls import path,re_path
from . import views

urlpatterns = [
    # 写博客首页
    re_path(r'^$', views.show,name='index_show'),
    # 上传图片
    re_path(r'^uploadimg/$', views.uploadimg,name='uploadimg'),
    re_path(r'^updatauser/$', views.updatauser,name='updatauser'),
    # 新建分分类专栏
    re_path(r'^addflzl/$',views.addflzl,name='addflzl'),
    # 新增博客
    re_path(r'^useradd_blog/$',views.useradd_blog,name='useradd_blog'),
    # 编辑博客
    # re_path(r'^edit_(?P<bid>[0-9]+)/$',views.edit_blog,name='edit_blog')


]