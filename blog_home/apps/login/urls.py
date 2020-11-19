# - * - coding:utf-8 - * -
from django.urls import path,re_path
from . import views

urlpatterns = [
    # 登陆首页
    re_path(r'^$', views.show,name='index_show'),
    # 验证码
    re_path(r'^checkma/$',views.checkma,name='checkma'),
    #检查图片验证 发送手机验证码
    re_path(r'^checkimgyzm/$',views.checkimgyzm,name='checkimgyzm'),
    # 注册
    re_path(r'^register/$',views.register,name='register'),
    # 忘记密码第一步
    re_path(r'^forgetpwd_1/$',views.forgetpwd_1,name='forgetpwd_1'),
    # 忘记密码第二布
    re_path(r'^forgetpwd_2/$',views.forgetpwd_2,name='forgetpwd_2'),
    # 忘记密码第三步
    re_path(r'^forgetpwd_3/$',views.forgetpwd_3,name='forgetpwd_3'),
    #退出
    re_path(r'^userlogout/$',views.userlogout,name='userlogout'),
]