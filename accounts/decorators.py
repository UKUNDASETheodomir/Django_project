from urllib import request
from django.shortcuts import redirect
from django.http import HttpResponse
from functools import wraps

def vendor_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'V':
            return func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper

def customer_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'C':
            return func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper