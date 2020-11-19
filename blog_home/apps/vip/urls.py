# - * - coding:utf-8 - * -
from django.urls import path,re_path
from . import views

urlpatterns = [
    # 写博客首页
    re_path(r'^$', views.show,name='index_show'),

]