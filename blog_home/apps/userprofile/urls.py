# - * - coding:utf-8 - * -
from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.show,name='index_show'),
    # 我的收藏
    re_path(r'^collection-list/$',views.collection_list,name='collection-list'),
    # 新建收藏夹
    re_path(r'^collection-list/addcollection',views.addcollection,name='addcollection'),
    # 查看收藏博客
    re_path(r'^collection-list/c_(?P<cid>[0-9]+)/$',views.col_list,name='col_list'),
    # 删除收藏夹
    re_path(r'delcol',views.delcol,name='delcol'),
    # 删除专栏
    re_path(r'delzl',views.delzl,name='delzl'),
    # 取消收藏
    re_path(r'^collection-list/c_(?P<cid>[0-9]+)/cancel_col',views.cancel_col,name='cancel_col'),
    # 我的博客
    re_path(r'^myblog/$',views.myblog,name='myblog'),
    # 查看收藏博客
    re_path(r'^myblog/zl_(?P<cid>[0-9]+)/$',views.bg_list,name='bg_list'),
    # 新建专栏 addflzl
    re_path(r'^myblog/addflzl',views.addflzl,name='addflzl'),
    # 删除博客
    re_path(r'^myblog/zl_(?P<cid>[0-9]+)/del_bg',views.del_bg,name='del_bg'),
    # 移动博客
    re_path(r'^myblog/zl_(?P<cid>[0-9]+)/move_bg',views.move_bg,name='move_bg'),
    # 评论管理
    re_path(r'^mycomment/$',views.mycomment,name='mycomment'),
    # 删除评论
    re_path(r'^mycomment/co_del',views.co_del,name='co_del')
]