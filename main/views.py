from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from users.models import Class, Teacher, Student, Parent
from django.http import HttpResponse
from .models import Attendence, Quiz, Challenge
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
        "usertype": usertype,
        "selected": category, # the currently selected category
        "fname": request.user.first_name,
        "lname": request.user.last_name,
        "email": request.user.email,
        "user_id": request.user.id,
        "profile_pic": request.user.userprofile.profile_pic.url,
    }

    if get_context(request, category) != None:
        context.update(get_context(request, category))

    return render(request, usertype_template_map.get(usertype), context)

@login_required
def challenge_view(request, id):
    question_list = get_challenge_questions(id)
    return HttpResponse(question_list[0].question)

def error_view(request):
    context = {
        "code": 404,
        "message": "page not found",
    }
    return render(request, "404.html", context)


# Get the context for each category
# TODO: add all the categories
def get_context(request, category):
    leaderboard = get_leaderboard()

    user_data = None
    user_type = get_user_type(request)

    context = {}
    if user_type == "student":
        context = {
            "user_data": request.user.student,
        }
        user_data = request.user.student
        if category == "dashboard":
            context = {
                "user_data": user_data,
                "leaderboard": leaderboard,
            }
            context["bmi"] = user_data.weight / (user_data.height * 0.308 * user_data.height * 0.308)
            context["required_xp"] = next_level(user_data.level)
            context["xp_progress"] = (int(user_data.xp) / context["required_xp"]) * 100;
            context["attendance"] = Attendence.objects.filter(student_id=request.user.student.id).values()[0]
            return context
        if category == "health":
            context["bmi"] = user_data.weight / (user_data.height * 0.308 * user_data.height * 0.308)
            context["weight_health"] = get_health_from_bmi(context["bmi"])
            return context
        if category == "quizzes":
            context["quiz_list"] = get_quiz(user_data.grade)
        if category == "challenges":
            context["challenges"] = get_challenges(user_data.grade)
    elif user_type == "parent":
        user_data = request.user.parent.students.all()
        children_data = []
        if category == "dashboard":
            for student in user_data:
                child_data = {}
                child_data["user_data"] = student
                child_data["bmi"] = student.weight / (student.height * 0.308 * student.height * 0.308)
                child_data["required_xp"] = next_level(student.level)
                child_data["xp_progress"] = (int(student.xp) / child_data["required_xp"]) * 100;
                child_data["attendance"] = Attendence.objects.filter(student_id=student.id).values()[0]
                children_data.append(child_data)
            context = {
                "children_data": children_data,
                "leaderboard": leaderboard,
            }
        if category == "health":
            for student in user_data:
                child_data = {}
                child_data["user_data"] = student
                child_data["bmi"] = student.weight / (student.height * 0.308 * student.height * 0.308)
                child_data["weight_health"] = get_health_from_bmi(child_data["bmi"])
                children_data.append(child_data)
            context = {
                "children_data": children_data,
            }
        if category == "progress":
            for student in user_data:
                child_data = {}
                child_data["user_data"] = student
            context = {
                "children_data": children_data,
            }

    if category == "leaderboard":
        return {
            "leaderboard": leaderboard,
        }


    # Default: return empty context
    return context