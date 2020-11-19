# - * - coding:utf-8 - * -
from django.shortcuts import render
from django.http import HttpResponse
import re

class AdminLoginMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_list = ['/login/']
        if re.match('/',request.path) and request.path not in url_list:
            if request.session.get('adminstrator','') == '':
                return render(request,'login.html',{
                    'jscode':"layer.msg('请先登录！',{anim:6})"
                })
        response = self.get_response(request)
        return response