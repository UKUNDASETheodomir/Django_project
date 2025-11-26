from urllib import request
from django.shortcuts import redirect
from django.http import HttpResponse


def unauthenticated_user(view_func):
    def wrapper_func(request, *args,**kwargs):
         if request.user.is_authenticated:
            return redirect('home')
         else: 
            return view_func(request, *args,**kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args,**kwargs):
             
              group = None
              if request.user.groups.exists():
                   group = request.user.groups.all()[0].name
              if group in allowed_roles:
                  return view_func(request, *args,**kwargs)
              else: 
               return HttpResponse('you are not authorized')
        return wrapper_func
    return decorator
def require_vendor(view_func):
    def wrapper_function(request, *args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.groups.all()[0].name

        if group == 'customer':
            return redirect('user')
        if group == 'vendor':
            return view_func(request, *args,**kwargs)
        
        return wrapper_function