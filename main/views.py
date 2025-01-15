from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from users.models import Class, Teacher, Student, Parent
from .config import SIDEBAR_ITEMS
from .utils import *

# Create your views here.
def index(request):
    return render(request, "main/index.html")

@login_required
def dashboard_view(request, category=None):
    if category is None:
        category = "dashboard"

    usertype = get_user_type(request)
    # Map usertype to the corresponding template file for the given category
    usertype_template_map = {
        "student": f"main/student/{category}.html",
        "parent": f"main/parent/{category}.html",
        "teacher": f"main/teacher/{category}.html",
    }

    context = {
        "sidebar_items": SIDEBAR_ITEMS.get(usertype), # list of sidebar categories + the path to the icons

        "username": request.user.username,
        "selected": category, # the currently selected category
        "fname": request.user.first_name,
        "lname": request.user.last_name,
        "email": request.user.email,
        "user_id": request.user.id
    }

    if get_context(request, category) != None:
        context.update(get_context(request, category))

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
    # Map the category to each of the fields that the page requires
    category_fields_map = {
        "dashboard": ["points", "height", "weight"],
        "health": ["height", "weight"],
        "leaderboard": ["user_id", "user__first_name", "user__last_name", "points"]
    }

    # Get the user data for specified category
    fields = {}
    if category in category_fields_map:
        fields = category_fields_map.get(category)

    leaderboard = get_user_data_all(request, *category_fields_map["leaderboard"])
    leaderboard = sorted(leaderboard, key=lambda x: x["points"], reverse=True)

    user_data = get_user_data(request, *fields)

    if category == "dashboard" or category == "health":
        user_data["bmi"] = user_data["weight"] / (user_data["height"] * 0.308 * user_data["height"] * 0.308)
        user_data["progress"] = 85; # FIXME: this is only example data
        user_data["attendance"] = 93; # FIXME: example data
        return {
            "user_data": user_data,
            "leaderboard": leaderboard,
        }
    if category == "health":
        user_data["bmi"] = user_data["weight"] / (user_data["height"] * 0.308 * user_data["height"] * 0.308)
        return {
            "user_data": user_data,
        }
    if category == "leaderboard":
        return {
            "leaderboard": leaderboard,
        }

    # Default: return user data only
    return {
        "user_data": user_data,
    }