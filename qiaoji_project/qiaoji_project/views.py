from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import UserTable
from rest_framework import permissions
from rest_framework_simplejwt import authentication
from rest_framework.views import APIView
from rest_framework.response import Response


# 默认跳转
def page_login(request):
    msg = request.session.get('login_msg', default=None)
    if not msg:
        msg = ''
    user_id = request.session.get('user_id', default=None)
    if not user_id:
        return render(request,'login.html',{'msg':msg})
    return render(request,'index.html',{'user_id':user_id,'msg':msg})

# 登录动作
def login(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.POST.get('username')
        data = UserTable.objects.filter(username=username).first()
        if not data:
            request.session['login_msg'] = '用户名不存在'
            request.session.set_expiry(0)
            return redirect('/')  # 用户名不存在
        user_id = data.user_id
        pwd = data.password
        if password != pwd:
            request.session['login_msg'] = '您的密码有误'
            request.session.set_expiry(0)
            return redirect('/')  # 密码错误
        request.session['user_id'] = user_id
        request.session.set_expiry(3600)
        request.session['login_msg'] = '登录成功'
        # request.session.set_expiry(0)
        return redirect('/')  # 登录成功，重定向主页
    else:
        return HttpResponse('您的地址有误')


# 注册
def page_registered(request):
    return render(request,'registered.html')

