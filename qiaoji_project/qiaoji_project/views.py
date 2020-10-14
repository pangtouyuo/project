from django.shortcuts import render,redirect
from rest_framework import permissions
from rest_framework_simplejwt import authentication
from rest_framework.views import APIView
from rest_framework.response import Response

def page_login(request):
    user_id = request.session.get('user_id', default=None)
    if not user_id:
        return render(request,'login.html')
    return render(request,'index.html',{'user_id':user_id})

def redirect_login(request):
    return redirect('/lab/login')

def page_registered(request):
    return render(request,'registered.html')



# class TestView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = (authentication.JWTAuthentication,)
#     def get(self, request, *args, **kwargs):
#         return Response('ok')