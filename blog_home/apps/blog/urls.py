# - * - coding:utf-8 - * -
# - * - coding:utf-8 - * -
from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.show,name='index_show'),
    #评论点赞
    re_path(r'^comment_affirm/$',views.comment_affirm,name='comment_affirm'),
    # 博客点赞
    re_path(r'^affirm_blog/$',views.affirm_blog,name='affirm_blog'),
    #添加收藏
    re_path(r'addcollection',views.addcollection,name='addcollection'),
    #收藏博客
    re_path(r'collectblog',views.collectblog,name='collectblog'),
]