from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, "main/index.html")

@login_required
def dashboard_view(request):
    usertype = request.user.groups.all()[0].name
    usertype_template_map = {
        "student": "main/student/dashboard.html",
        "parent": "main/parent/dashboard.html",
        "teacher": "main/teacher/dashboard.html",
    }
    context = {
        "username": request.user.username,
    }
        
    return render(request, usertype_template_map.get(usertype), context)


@login_required
def dashboard_category_view(request, category):
    usertype = request.user.groups.all()[0].name
    usertype_template_map = {
        "student": f"main/student/{category}.html",
        "parent": f"main/parent/{category}.html",
        "teacher": f"main/teacher/{category}.html",
    }
    return render(request, usertype_template_map.get(usertype))

def error_view(request):
    context = {
        "code": 404,
        "message": "page not found",
    }
    return render(request, "error.html", context)