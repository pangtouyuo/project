from django.urls import path,re_path,include
from . import views


urlpatterns = [
    path('page_registered', views.page_registered),
    path('login', views.login),
    path('lab/out_login', views.out_login),
    path('lab/', views.page_lab),
    path('lab/details/<order_id>',views.details),
    path('lab/delete/<order_id>',views.delete_order)
    # re_path(r'^api/login/$',views.LoginView.as_view())
]