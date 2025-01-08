from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def dashboard_view(request):
    context = {
        'usertype': 'student',
    }
    return render(request, "main/dashboard.html", context)