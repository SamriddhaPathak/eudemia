from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .config import SIDEBAR_ITEMS

# Create your views here.
def index(request):
    return render(request, "main/index.html")

@login_required
def dashboard_view(request):
    usertype = request.user.groups.all()[0].name # FIXME: get from database instead
    usertype_template_map = {
        "student": "main/student/dashboard.html",
        "parent": "main/parent/dashboard.html",
        "teacher": "main/teacher/dashboard.html",
    }
    context = {
        "username": request.user.username,
        "sidebar_items": SIDEBAR_ITEMS.get(usertype),
        "selected": "dashboard",
    }
        
    return render(request, usertype_template_map.get(usertype), context)


@login_required
def dashboard_category_view(request, category):
    usertype = request.user.groups.all()[0].name # FIXME: get from database instead

    # Map usertype to the corresponding template file for the given category
    usertype_template_map = {
        "student": f"main/student/{category}.html",
        "parent": f"main/parent/{category}.html",
        "teacher": f"main/teacher/{category}.html",
    }

    context = {}
    if get_context(request, category) != None:
        context.update(get_context(request, category))
    context.update({
        "sidebar_items": SIDEBAR_ITEMS.get(usertype), # list of sidebar categories + the path to the icons
        "username": request.user.username,
        "selected": category, # the currently selected category
    })

    return render(request, usertype_template_map.get(usertype), context)

def error_view(request):
    context = {
        "code": 404,
        "message": "page not found",
    }
    return render(request, "404.html", context)

# Get the context for each category
# TODO: add all the categories
def get_context(request, category):
    if category == "leaderboard":
        return {
            # FIXME: example leaderboard data
            "leaderboard": [
                {'name': 'Liam', 'points': 500},
                {'name': 'Olivia', 'points': 496},
                {'name': 'Noah', 'points': 492},
                {'name': 'Emma', 'points': 488},
                {'name': 'Oliver', 'points': 484},
                {'name': 'Ava', 'points': 480},
                {'name': 'Elijah', 'points': 476},
                {'name': 'Sophia', 'points': 472},
                {'name': 'James', 'points': 468},
                {'name': 'Isabella', 'points': 464},
                {'name': 'William', 'points': 460},
                {'name': 'Mia', 'points': 456},
                {'name': 'Benjamin', 'points': 452},
                {'name': 'Charlotte', 'points': 448},
                {'name': 'Lucas', 'points': 444},
                {'name': 'Amelia', 'points': 440},
                {'name': 'Henry', 'points': 436},
                {'name': 'Harper', 'points': 432},
                {'name': 'Theodore', 'points': 428},
                {'name': 'Evelyn', 'points': 424},
                {'name': 'Jack', 'points': 420},
                {'name': 'Abigail', 'points': 416},
                {'name': 'Levi', 'points': 412},
                {'name': 'Ella', 'points': 408},
                {'name': 'Alexander', 'points': 404},
                {'name': 'Elizabeth', 'points': 400},
                {'name': 'Jackson', 'points': 396},
                {'name': 'Camila', 'points': 392},
                {'name': 'Sebastian', 'points': 388},
                {'name': 'Luna', 'points': 384},
                {'name': 'Mateo', 'points': 380},
                {'name': 'Sofia', 'points': 376},
                {'name': 'Daniel', 'points': 372},
                {'name': 'Avery', 'points': 368},
                {'name': 'Michael', 'points': 364},
            ]
        }