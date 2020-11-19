"""joinus_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,re_path
from . import views
urlpatterns = [
    re_path(r'^$',views.show,name='adminperssion_show'),
    #新增管理员
    re_path(r'^adminuseradd/$',views.adminuseradd,name='adminuseradd'),
    #验证 checkadminperssionuser
    re_path(r'^checkadminperssionuser/$',views.checkadminperssionuser,name='checkadminperssionuser'),
    #编辑请求数据
    re_path(r'^edit_this/$',views.edit_this,name='edit_this'),
    #提交编辑
    re_path(r'^edit_submit/$',views.edit_submit,name='edit_submit'),
    #删除 strator
    re_path(r'^delthis/$',views.delthis,name='delthis'),
    #重置密码
    re_path(r'^resetpwd/$',views.resetpwd,name='resetpwd'),


]
