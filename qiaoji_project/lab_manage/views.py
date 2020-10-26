from django.http import JsonResponse
from . import models
from .val_session import *
from django.shortcuts import render,HttpResponse,redirect
import time,datetime,re
import uuid


# 下划线命名变驼峰命名
def change_name(table_name):
    arr = table_name.split('_')
    res = ''
    for i in arr:
        res = res + i[0].upper() + i[1:]
    if not bool:
        res = res[0].lower() + res[1:]
    return res


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
    table_name = change_name(table_name)
    str = 'models.'+table_name+'.objects.all().values()'
    data = eval(str)
    # data = list(data)
    # return JsonResponse(data,safe=False)
    return render(request, 'lab_manage/lab_manager.html', {'data':data,'username':username})


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


# 添加页渲染
def new_order(request):
    user_id = request.session.get('user_id')
    if not user_id:
        request.session['login_msg'] = '您的登录已过期'
        request.session.set_expiry(0)
        return redirect('/')
    company_id = models.UserTable.objects.filter(user_id=user_id).first().company
    data_table = models.CompanyLevel.objects.filter(id=company_id).first().inf_table_name
    table_name = change_name(data_table)
    equi_data = models.Equipment.objects.filter(company_id=company_id).values()
    return render(request,'lab_manage/create.html',{'table':table_name,'equi_data':equi_data})


# 添加新订单
def create_order(request):
    if request.method =='POST':
        order_name = request.POST.get('order_name')
        table_name = request.POST.get('table_name')
        print(table_name)
        data_str = 'models.'+table_name+'.objects.filter(order_name=order_name).first()'

        data = eval(data_str)
        if data:
            return JsonResponse({'msg':'1'})
        test_name = request.POST.get('test_name')
        content = request.POST.get('content')
        number = request.POST.get('number')
        code = request.POST.get('equipment_name')
        customer_name = request.POST.get('customer_name')
        tester_name = request.POST.get('tester_name')
        state = '未开始'
        predict_end_time = request.POST.get('predict_end_time').replace("T", " ")+':00'
        note = request.POST.get('note')

        uid = str(uuid.uuid1())
        create_str = 'models.'+table_name+'.objects.create(id=uid,order_name=order_name,test_name=test_name,content=content,'
        create_str = create_str+'number=number,code=code,customer_name=customer_name,tester_name=tester_name,state="未开始",predict_end_time=predict_end_time,note=note)'
        eval(create_str)
        str_0 = 'mod'
        return redirect('details/'+uid)


# 删除单号
def delete_order(request,order_id):
    user_id = request.session.get('user_id')
    if not user_id:
        request.session['login_msg'] = '您的登录已过期'
        request.session.set_expiry(0)
        return redirect('/')
    try:
        company_id = models.UserTable.objects.filter(user_id=user_id).first().company
        table_name = models.CompanyLevel.objects.filter(id=company_id).first().inf_table_name
        table_name = change_name(table_name)
        str_1 = 'models.'+table_name+'.objects.filter(id=order_id).delete()'
        eval(str_1)
        return JsonResponse({'msg':'1'})
    except:
        return JsonResponse({'msg':'0'})


# 详情页渲染
def details(request,order_id):
    user_id = request.session.get('user_id')
    if not user_id:
        request.session['login_msg'] = '您的登录已过期'
        request.session.set_expiry(0)
        return redirect('/')
    company_id = models.UserTable.objects.filter(user_id=user_id).first().company
    table_name = models.CompanyLevel.objects.filter(id=company_id).first().inf_table_name
    table_name = change_name(table_name)
    str = 'models.' + table_name + '.objects.filter(id=order_id).values()'
    data = eval(str)
    return render(request,'lab_manage/details.html',{'data':data,'table':table_name})


# 点击测试项开始按钮动作
def order_begin(request):
    user_id = request.session.get('user_id')
    if not user_id:
        request.session['login_msg'] = '您的登录已过期'
        request.session.set_expiry(0)
        return redirect('/')
    table_name = request.POST.get('table_name')
    order_id = request.POST.get('order_id')
    now_time = time.strftime('%Y-%m-%d %H:%M:%S')
    print(now_time)
    str1 = 'models.' + table_name + '.objects.filter(id=order_id).update(start_time=now_time)'
    eval(str1)
    str2 = 'models.' + table_name + '.objects.filter(id=order_id).update(state="进行中")'
    eval(str2)
    return JsonResponse({'msg':'success'})
    # return redirect('details/'+order_id)


# 查看设备
def select_equipment(request,equipment_id):
    pass


# 暂停操作
def pause(request):
    user_id = request.session.get('user_id')
    if not user_id:
        request.session['login_msg'] = '您的登录已过期'
        request.session.set_expiry(0)
        return redirect('/')
    table_name = request.POST.get('table_name')
    order_id = request.POST.get('order_id')
    now_time = time.strftime('%Y-%m-%d %H:%M:%S')
    this_uid = uuid.uuid1()
    models.PauseData.objects.create(id=this_uid,order_id=order_id,pause_time=now_time)
    str_1 = 'models.' + table_name + '.objects.filter(id=order_id).update(state="暂停中")'
    eval(str_1)
    str_2 = 'models.' + table_name + '.objects.filter(id=order_id).update(pause_id=this_uid)'
    eval(str_2)
    return JsonResponse({'msg': '1111'})


# 重新启动
def start(request):
    user_id = request.session.get('user_id')
    if not user_id:
        request.session['login_msg'] = '您的登录已过期'
        request.session.set_expiry(0)
        return redirect('/')
    table_name = request.POST.get('table_name')
    order_id = request.POST.get('order_id')
    pause_id = request.POST.get('pause_id')
    now_time = time.strftime('%Y-%m-%d %H:%M:%S')
    models.PauseData.objects.filter(id=pause_id).update(start_time=now_time)
    str_1 = 'models.' + table_name + '.objects.filter(id=order_id).update(state="进行中")'
    eval(str_1)
    return HttpResponse('111')


# 结束
def order_end(request):
    user_id = request.session.get('user_id')
    if not user_id:
        request.session['login_msg'] = '您的登录已过期'
        request.session.set_expiry(0)
        return redirect('/')
    table_name = request.POST.get('table_name')
    order_id = request.POST.get('order_id')
    now_time = time.strftime('%Y-%m-%d %H:%M:%S')
    data = models.PauseData.objects.filter()
    str_1 = 'models.' + table_name + '.objects.filter(id=order_id).update(end_time=now_time)'
    eval(str_1)
    str_2 = 'models.' + table_name + '.objects.filter(id=order_id).update(state="已结束")'
    eval(str_2)
    return HttpResponse('1')


# 按设备搜索
def select_order(request):
    user_id = request.session.get('user_id')
    equipment_name = request.POST.get('equipment_name')
    if not user_id:
        request.session['login_msg'] = '您的登录已过期'
        request.session.set_expiry(0)
        return redirect('/')

    data = models.UserTable.objects.filter(user_id=user_id).first()
    company_id = data.company

    equipment_data = models.Equipment.objects.filter(equipment_name=equipment_name).first()
    print(equipment_data)

    if not equipment_data:
        data = ['查无此设备']
        return JsonResponse(data,safe=False)
    company_id_eq = equipment_data.company_id

    if company_id != company_id_eq:
        data = ['查无此设备']
        return JsonResponse(data, safe=False)

    table_name = models.CompanyLevel.objects.filter(id=company_id).first().inf_table_name
    table_name = change_name(table_name)
    str = 'models.'+table_name+'.objects.filter(code=equipment_name).values()'
    data = eval(str)
    data = list(data)

    return JsonResponse(data,safe=False)





























