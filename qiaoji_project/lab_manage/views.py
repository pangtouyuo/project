from django.http import JsonResponse
from . import models
from .val_session import *
from django.shortcuts import render,HttpResponse

# 注册页（未开放）
def page_registered(request):
    return render(request,'registered.html')


# 登录动作
def login(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.POST.get('username')
        data = models.UserTable.objects.filter(username=username).first()
        if not data:
            return render(request,'login.html',{'msg':'用户名不存在'})
        user_id = data.user_id
        pwd = data.password
        if password != pwd:
            return render(request,'login.html',{'msg':'密码错误'})
        request.session['user_id'] = user_id
        request.session.set_expiry(3600)
        return render(request,'index.html', {'msg': '登陆成功','user_id':user_id})
    else:
        user_id = request.session.get('user_id')
        if not user_id:
            return render(request,'login.html',{'msg':'请先登录'})
        return render(request,'index.html',{'msg':'你好'})


# 退出登录
def out_login(request):
    try:
        del request.session['user_id']
        return render(request, 'login.html', {'msg': '您已退出，请重新登录'})
    except:
        return HttpResponse('操作失败')


# 实验室管理系统主页渲染
# @ValidationSession
def page_lab(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'login.html', {'msg': '您的登录已过期'})
    username = models.UserTable.objects.filter(user_id=user_id).first().username
    data = models.TestInformation.objects.all().values()
    return render(request, 'lab_manage/lab_manager.html', {'data':data,'username':username})


# # 添加页渲染
# @ValidationSession
# def create_new_order(request):
#     return render(request,'lab_manage/create.html')
#
#
# # 修改密码
# def update_pwd(request):
#     return render(request,'')


# 详情页渲染
def details(request,order_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'login.html', {'msg': '您的登录已过期'})
    data = models.TestInformation.objects.filter(id=order_id).values()
    return render(request,'lab_manage/details.html',{'data':data})


# 删除单号
def delete_order(request,order_id):
    try:
        models.TestInformation.objects.filter(id=order_id).delete()
        return JsonResponse({'msg':'删除成功'})
    except:
        return JsonResponse({'msg':'删除失败'})


# # 订单开始
# def update_state(request,order_id):
#     data = models.TestInformation.objects.filter(id=order_id)
#     state = data.state
#     if state == '进行中':
#         state = ''
#         pass
