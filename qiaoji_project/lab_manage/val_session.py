from django.shortcuts import render

# user_id = request.session.get('user_id')
# if not user_id:
#     return render(request,'login.html',{'msg':'您的登录已过期'})


def ValidationSession(func):
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get("user_id", None)
        if not user_id:
            return render(request, "login.html",{'msg':'您的登录已过期'})
        else:
            user_id = user_id
            res = func(request,user_id, *args, **kwargs)
            return res
    return wrapper