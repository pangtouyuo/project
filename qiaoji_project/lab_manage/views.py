from django.http import JsonResponse
from . import models
from .val_session import *
from django.shortcuts import render,HttpResponse,redirect
import time,datetime


# 注册页（未开放）
def page_registered(request):
    return render(request,'registered.html')

# 退出登录
def out_login(request):
    try:
        request.session.flush()
        request.session['login_msg'] = '您已退出，请重新登录'
        request.session.set_expiry(0)
        return redirect('/')
    except:
        return HttpResponse('操作失败')


# 实验室管理系统主页渲染
def page_lab(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/', {'msg': '您的登录已过期'})
    username = models.UserTable.objects.filter(user_id=user_id).first().username
    data = models.TestInformation.objects.all().values()
    return render(request, 'lab_manage/lab_manager.html', {'data':data,'username':username})


# 添加页渲染
# @ValidationSession
def new_order(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'login.html', {'msg': '您的登录已过期'})
    return render(request,'lab_manage/create.html')


# 添加新订单
def create_order(request):
    if request.method =='POST':
        order_name = request.POST.get('order_name')
        data = models.TestInformation.objects.filter(order_name=order_name).first()
        if data:
            return JsonResponse({'msg':'单号已存在'})
        test_name = request.POST.get('order_name')
        content = request.POST.get('content')
        number = request.POST.get('number')
        code = request.POST.get('code')
        customer_name = request.POST.get('customer_name')
        tester_name = request.POST.get('tester_name')
        state = '未开始'
        note = request.POST.get('note')
        result = models.TestInformation.objects.create(order_name=order_name,
                                                       test_name=test_name,
                                                       content=content,
                                                       number=number,
                                                       code=code,
                                                       customer_name=customer_name,
                                                       tester_name=tester_name,
                                                       state=state,
                                                       note=note)
        result.save()
        return JsonResponse({'msg':'创建成功'})


# 点击测试项开始按钮动作
# def order_begin(request):


# 修改密码
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


# 订单结束
# def  finish_state(request,order_id):
#     end_time = datetime.datetime


# 查看设备
def select_equipment(request,equipment_id):
    pass

