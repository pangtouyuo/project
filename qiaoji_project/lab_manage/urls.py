from django.urls import path,re_path,include
from . import views


urlpatterns = [
    path('page_registered', views.page_registered),
    path('login', views.login),
    path('out_login', views.out_login),
    path('', views.page_lab),
    path('details/<order_id>',views.details),
    path('delete/<order_id>',views.delete_order),
    path('add',views.new_order)
    # re_path(r'^api/login/$',views.LoginView.as_view())
]