"""blog_admin URL Configuration

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
from django.urls import path,include


urlpatterns = [
    path('', include(('apps.index.urls','index')),name='index'),
    path('user/',include(('apps.user.urls','user')),name='user'),
    path('blog/',include(('apps.blog.urls','blog')),name='blog'),
    path('blogcate/',include(('apps.blogcate.urls','blogcate')),name='blogcate'),
    path('vip/',include(('apps.vip.urls','vip')),name='vip'),
    path('banner/',include(('apps.banner.urls','banner')),name='banner'),
    path('adminperssion/',include(('apps.adminperssion.urls','adminperssion')),name='adminperssion'),
]
