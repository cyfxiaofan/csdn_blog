from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.show,name='index_show'),
    re_path(r'^lyban/$',views.lyban,name='lyban'),
]