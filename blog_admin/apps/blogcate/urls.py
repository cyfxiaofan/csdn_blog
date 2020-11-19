# - * - coding:utf-8 - * -
from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.Show.as_view(),name='blogcate_show'),
    #新增博客分类
    re_path(r'^addblogcate/$', views.Addblogcate.as_view(),name='addblogcate'),
    #验证博客分类name
    re_path(r'^checkblogcatename/$',views.Checkblogcatename.as_view(),name='checkblogcatename'),
    #验证博客分类path
    re_path(r'^checkblogcatepath/$',views.Checkblogcatepath.as_view(),name='checkblogcatepath'),
    #编辑
    re_path(r'^editblogcate/$',views.Editblogcate.as_view(),name='editblogcate'),
    #逻辑删除
    re_path(r'^delthis/$',views.Delthis.as_view(),name='delthis')
]