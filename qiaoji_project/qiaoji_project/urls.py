"""qiaoji_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,re_path,include
from . import views
# from .views import TestView
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    path('lab/',include('lab_manage.urls')),
    # path('admin/', admin.site.urls),
    re_path('^$', views.page_login),
    # re_path(r'^api/auth/token/obtain/$', TokenObtainPairView.as_view()),    # 需要添加的内容
    # re_path(r'^api/auth/token/refresh/$', TokenRefreshView.as_view()),    # 需要添加的内容
    # re_path(r'^api/test/$', TestView.as_view()),    # 添加测试views的路由

]
