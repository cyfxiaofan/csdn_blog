"""blog_home URL Configuration

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
from django.urls import re_path,include


urlpatterns = [
    re_path('', include(('apps.index.urls','index')),name='index'),
    re_path(r'^user_(?P<uid>[0-9]+)/blog_(?P<bid>[0-9]+)/', include(('apps.blog.urls','blog')),name='blog'),
    re_path(r'^user_(?P<uid>[0-9]+)/', include(('apps.usermession.urls','user')),name='user'),
    re_path(r'^login/',include(('apps.login.urls','login')),name='login'),
    re_path(r'^writeblog/',include(('apps.writeblog.urls','writeblog')),name='writeblog'),
    re_path(r'^userprofile/',include(('apps.userprofile.urls','userprofile')),name='userprofile'),
    re_path(r'^vip/',include(('apps.vip.urls','vip')),name='vip'),
]