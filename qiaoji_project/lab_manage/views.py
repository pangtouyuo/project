from django.http import JsonResponse
from . import models
from .val_session import *
from django.shortcuts import render,HttpResponse,redirect
import time,datetime,re
import uuid


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
        request.session['login_msg'] = '您的登录已过期'
        request.session.set_expiry(0)
        return redirect('/')
    data = models.UserTable.objects.filter(user_id=user_id).first()
    username = data.username
    company_id = data.company
    table_name = models.CompanyLevel.objects.filter(id=company_id).first().inf_table_name
    arr = table_name.split('_')
    res = ''
    for i in arr:
        res = res + i[0].upper()+i[1:]
    if not bool:
        res = res[0].lower() + res[1:]
    str = 'models.'+res+'.objects.all().values()'
    data = eval(str)
    return render(request, 'lab_manage/lab_manager.html', {'data':data,'username':username})


# 添加页渲染
# @ValidationSession
def new_order(request):
    user_id = request.session.get('user_id')
    if not user_id:
        request.session['login_msg'] = '您的登录已过期'
        request.session.set_expiry(0)
        return redirect('/')
    company_id = models.UserTable.objects.filter(user_id=user_id).first().company
    data_table = models.CompanyLevel.objects.filter(id=company_id).first().inf_table_name
    return render(request,'lab_manage/create.html',{'table':data_table})
    # return HttpResponse('111')

# 添加新订单
def create_order(request):
    if request.method =='POST':
        order_name = request.POST.get('order_name')
        table_name = request.POST.get('table_name')
        print(table_name)
        arr = table_name.split('_')
        res = ''
        for i in arr:
            res = res + i[0].upper() + i[1:]
        if not bool:
            res = res[0].lower() + res[1:]

        data_str = 'models.'+res+'.objects.filter(order_name=order_name).first()'
        print(data_str)
        data = eval(data_str)
        if data:
            return JsonResponse({'msg':'1'})
        test_name = request.POST.get('order_name')
        content = request.POST.get('content')
        number = request.POST.get('number')
        code = request.POST.get('code')
        customer_name = request.POST.get('customer_name')
        tester_name = request.POST.get('tester_name')
        state = '未开始'
        note = request.POST.get('note')
        dict = {}

        return JsonResponse({'msg':'2'})


# 点击测试项开始按钮动作
# def order_begin(request):


# 修改密码页渲染
def change_pwd(request):
    user_id = request.session.get('user_id')
    if not user_id:
        request.session['login_msg'] = '您的登录已过期'
        request.session.set_expiry(0)
        return redirect('/')
    return render(request,'lab_manage/change_pwd.html',{'user_id':user_id})


# 修改密码动作
def update_pwd(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        pwd_1 = request.POST.get('pwd1')
        pwd_2 = request.POST.get('pwd2')
        pwd_3 = request.POST.get('pwd3')
        user_data = models.UserTable.objects.filter(user_id=user_id).first()
        if not user_data:
            return HttpResponse('未知错误')
        old_pwd = user_data.password
        if pwd_1 != old_pwd:
            return HttpResponse('旧密码错误')
        if pwd_2 != pwd_3:
            return HttpResponse('两次输入的新密码不一致')
        models.UserTable.objects.filter(user_id=user_id).update(password=pwd_2)
        return HttpResponse('新密码修改成功')


# 详情页渲染
def details(request,order_id):
    user_id = request.session.get('user_id')
    if not user_id:
        request.session['login_msg'] = '您的登录已过期'
        request.session.set_expiry(0)
        return redirect('/')
    company_id = models.UserTable.objects.filter(user_id=user_id).first().company

    table_name = models.CompanyLevel.objects.filter(id=company_id).first().inf_table_name
    arr = table_name.split('_')
    res = ''
    for i in arr:
        res = res + i[0].upper() + i[1:]
    if not bool:
        res = res[0].lower() + res[1:]
    str = 'models.' + res + '.objects.filter(id=order_id).values()'
    data = eval(str)
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

