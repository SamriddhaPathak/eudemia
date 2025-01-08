from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def dashboard_view(request):
    usertype = "parent"
    usertype_template_map = {
        "student": "main/student/dashboard.html",
        "parent": "main/parent/dashboard.html",
        "teacher": "main/teacher/dashboard.html",
    }
    return render(request, usertype_template_map.get(usertype))

def dashboard_category_view(request, category):
    usertype = "parent"
    usertype_template_map = {
        "student": f"main/student/{category}.html",
        "parent": f"main/parent/{category}.html",
        "teacher": f"main/teacher/{category}.html",
    }
    return render(request, usertype_template_map.get(usertype))