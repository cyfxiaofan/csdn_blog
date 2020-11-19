# - * - coding:utf-8 - * -
from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.show,name='index_show'),
    re_path(r'^404/$', views.pnf,name='pnf'),
    re_path(r'^search/$',views.search,name='search')
]