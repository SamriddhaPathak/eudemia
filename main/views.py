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
    context = get_context(request, category)
    return render(request, usertype_template_map.get(usertype), context)

def error_view(request):
    context = {
        "code": 404,
        "message": "page not found",
    }
    return render(request, "error.html", context)

def get_context(request, category):
    if category == "leaderboard":
        return {
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
                {'name': 'Mila', 'points': 360},
                {'name': 'Mason', 'points': 356},
                {'name': 'Aria', 'points': 352},
                {'name': 'Ethan', 'points': 348},
                {'name': 'Scarlett', 'points': 344},
                {'name': 'Logan', 'points': 340},
                {'name': 'Penelope', 'points': 336},
                {'name': 'Owen', 'points': 332},
                {'name': 'Layla', 'points': 328},
                {'name': 'Samuel', 'points': 324},
                {'name': 'Chloe', 'points': 320},
                {'name': 'Jacob', 'points': 316},
                {'name': 'Victoria', 'points': 312},
                {'name': 'Asher', 'points': 308},
                {'name': 'Madison', 'points': 304},
                {'name': 'Aiden', 'points': 300},
                {'name': 'Eleanor', 'points': 296},
                {'name': 'John', 'points': 292},
                {'name': 'Grace', 'points': 288},
                {'name': 'Joseph', 'points': 284},
                {'name': 'Nora', 'points': 280},
                {'name': 'Wyatt', 'points': 276},
                {'name': 'Riley', 'points': 272},
                {'name': 'David', 'points': 268},
                {'name': 'Zoey', 'points': 264},
                {'name': 'Leo', 'points': 260},
                {'name': 'Hannah', 'points': 256},
                {'name': 'Luke', 'points': 252},
                {'name': 'Hazel', 'points': 248},
                {'name': 'Julian', 'points': 244},
                {'name': 'Lily', 'points': 240},
                {'name': 'Hudson', 'points': 236},
                {'name': 'Ellie', 'points': 232},
                {'name': 'Grayson', 'points': 228},
                {'name': 'Violet', 'points': 224},
                {'name': 'Matthew', 'points': 220},
                {'name': 'Lillian', 'points': 216},
                {'name': 'Ezra', 'points': 212},
                {'name': 'Zoe', 'points': 208},
                {'name': 'Gabriel', 'points': 204},
                {'name': 'Stella', 'points': 200},
                {'name': 'Carter', 'points': 196},
                {'name': 'Aurora', 'points': 192},
                {'name': 'Isaac', 'points': 188},
                {'name': 'Natalie', 'points': 184},
                {'name': 'Jayden', 'points': 180},
                {'name': 'Emilia', 'points': 176},
                {'name': 'Landon', 'points': 172},
                {'name': 'Everly', 'points': 168},
                {'name': 'Eli', 'points': 164},
                {'name': 'Leah', 'points': 160},
                {'name': 'Nathan', 'points': 156},
                {'name': 'Aubrey', 'points': 152},
                {'name': 'Isaiah', 'points': 148},
                {'name': 'Willow', 'points': 144},
                {'name': 'Andrew', 'points': 140},
                {'name': 'Addison', 'points': 136},
                {'name': 'Thomas', 'points': 132},
                {'name': 'Lucy', 'points': 128},
                {'name': 'Joshua', 'points': 124},
                {'name': 'Audrey', 'points': 120},
                {'name': 'Caleb', 'points': 116},
                {'name': 'Bella', 'points': 112},
                {'name': 'Ryan', 'points': 108},
                {'name': 'Nova', 'points': 104},
                {'name': 'Liam', 'points': 100}
            ]
        }