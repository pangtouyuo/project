from django.urls import path,re_path,include
from . import views


urlpatterns = [
    path('page_registered', views.page_registered),
    # path('login/', views.login),                    # 登录
    path('out_login', views.out_login),            # 退出登录
    path('', views.page_lab),                      # 实验页渲染
    path('details/<order_id>',views.details),      # 详情页渲染
    path('delete/<order_id>',views.delete_order),  # 删除订单
    path('add',views.new_order)                    # 添加页渲染
    # re_path(r'^api/login/$',views.LoginView.as_view())
]