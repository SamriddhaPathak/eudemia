from django.http import HttpResponse
from django.shortcuts import redirect
from .utils import get_user_type

def teacher_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        usertype = get_user_type(request)
        if usertype == "teacher":
            return view_func(request, *args, **kwargs)
        else :
            return redirect("dashboard")
    
    return wrapper_func
