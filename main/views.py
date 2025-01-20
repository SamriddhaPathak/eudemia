from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from users.models import Class, Teacher, Student, Parent
from django.http import HttpResponse
from .models import Attendence, Quiz, Challenge, QuizTracker, ChallengeTracker, Quote
from .config import SIDEBAR_ITEMS
from .utils import *
from .decorators import teacher_only
from .forms import HealthEditForm, ChallengeCreateForm, ChallengeQuestionCreateForm

# Create your views here.
def index(request):
    return render(request, "main/index.html")

@login_required
def dashboard_view(request, category=None):
    if category is None:
        category = "dashboard"

    usertype = get_user_type(request)
    template = f"main/{usertype}/{category}.html"

    context = {
        "sidebar_items": SIDEBAR_ITEMS.get(usertype), # list of sidebar categories + the path to the icons

        "user": request.user,
        "usertype": usertype,
        "selected": category, # the currently selected category
        "profile_pic": request.user.userprofile.profile_pic.url,
        "quote": get_random_quote(),
    }

    if get_context(request, category) != None:
        context.update(get_context(request, category))

    return render(request, template, context)

@login_required
def challenge_view(request, id):
    student = request.user.student
    progress = get_object_or_404(ChallengeTracker, student=student, challenge_id=id)
    usertype = "student"

    # Get uncompleted questions
    all_questions = progress.challenge.question_set.all()
    correct_questions = progress.correct_questions.all()
    incorrect_questions = progress.incorrect_questions.all()
    completed_questions = progress.completed_questions()
    uncompleted_questions = all_questions.difference(completed_questions)

    if uncompleted_questions.exists():
        next_question = uncompleted_questions.first()
        return redirect("challenge_question", id=next_question.id)
    else:
        context = {
            "sidebar_items": SIDEBAR_ITEMS.get(usertype), # list of sidebar categories + the path to the icons

            "user": request.user,
            "usertype": usertype,
            "selected": "challenges", # the currently selected category
            "profile_pic": request.user.userprofile.profile_pic.url,
            "quote": get_random_quote(),
            "challenge_tracker": progress,
        }
        progress.grant_rewards()
        return render(request, "main/student/challenge_complete.html", context)

@login_required
def challenge_question_view(request, id):
    question = get_object_or_404(Question, id=id)
    student = request.user.student
    progress = ChallengeTracker.objects.filter(student=student, challenge=question.challenge).first()

    usertype = "student"
    context = {
        "sidebar_items": SIDEBAR_ITEMS.get(usertype), # list of sidebar categories + the path to the icons

        "user": request.user,
        "usertype": usertype,
        "selected": "challenges", # the currently selected category
        "profile_pic": request.user.userprofile.profile_pic.url,

        "question": question,
    }

    if request.method == "POST":
        answer = request.POST.get("answer")
        progress.answer = answer
        if answer == question.answer:
            progress.correct_questions.add(question)
        else:
            progress.incorrect_questions.add(question)
        progress.save()
        return redirect("challenge", id=progress.challenge.id)
    return render(request, "main/student/challenge.html", context)

@login_required
@teacher_only
def health_edit_view(request, id):
    student = get_object_or_404(Student, id=id)
    usertype = "teacher"

    if request.method == "POST":
        form = HealthEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Health details updated successfully")
            return redirect("dashboard_category", category="health")
    else:
        form = HealthEditForm(instance=student)

    context = {
        "sidebar_items": SIDEBAR_ITEMS.get(usertype), # list of sidebar categories + the path to the icons

        "user": request.user,
        "student": student,
        "usertype": usertype,
        "selected": "health", # the currently selected category
        "profile_pic": request.user.userprofile.profile_pic.url,
        "form": form,
    }
    return render(request, "main/teacher/health_edit.html", context)

@login_required
@teacher_only
def challenge_create_view(request):
    usertype = "teacher"

    if request.method == "POST":
        form = ChallengeCreateForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.created_by = request.user.teacher
            challenge.grade = request.user.teacher.grade
            challenge.save()
            messages.success(request, "Challenge created successfully")
            return redirect("challenge_question_create", challenge_id=challenge.id)
    else:
        form = ChallengeCreateForm()

    context = {
        "sidebar_items": SIDEBAR_ITEMS.get(usertype), # list of sidebar categories + the path to the icons

        "user": request.user,
        "usertype": usertype,
        "selected": "challenges", # the currently selected category
        "profile_pic": request.user.userprofile.profile_pic.url,
        "form": form,
    }
    return render(request, "main/teacher/create_challenge.html", context)

@login_required
@teacher_only
def challenge_delete_view(request, id):
    usertype = "teacher"

    challenge = get_object_or_404(Challenge, id=id)
    if request.method == "POST":
        challenge.delete()
        messages.success(request, "Challenge deleted successfully")
        return redirect("dashboard_category", category="challenges")

    context = {
        "sidebar_items": SIDEBAR_ITEMS.get(usertype), # list of sidebar categories + the path to the icons

        "user": request.user,
        "usertype": usertype,
        "selected": "challenges", # the currently selected category
        "profile_pic": request.user.userprofile.profile_pic.url,
        "challenge": challenge,
    }
    return render(request, "main/teacher/delete_challenge.html", context)

@login_required
@teacher_only
def challenge_question_create_view(request, challenge_id):
    usertype = "teacher"
    challenge = get_object_or_404(Challenge, id=challenge_id)

    if request.method == "POST":
        form = ChallengeQuestionCreateForm(request.POST)
        if form.is_valid():
            action = request.POST.get("action")
            question = form.save(commit=False)
            question.challenge = challenge
            question.question_type = challenge.challenge_type
            question.grade = challenge.grade
            question.subject = challenge.subject
            question.save()
            messages.success(request, "Question created")
            if action == "create":
                return redirect("challenge_question_create", challenge_id)
            else:
                return redirect("dashboard_category", "challenges")
    else:
        form = ChallengeQuestionCreateForm()

    context = {
        "sidebar_items": SIDEBAR_ITEMS.get(usertype), # list of sidebar categories + the path to the icons

        "user": request.user,
        "usertype": usertype,
        "selected": "challenges", # the currently selected category
        "profile_pic": request.user.userprofile.profile_pic.url,
        "challenge_id": challenge.id,
        "challenge": challenge,
        "form": form,
    }
    return render(request, "main/teacher/create_question.html", context)

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
            context["challenges"] = get_challenges(user_data.grade)
            context["completed_challenges"] = []
            context["challenges_count"] = []
            context["completed_challenges_percentage"] = []
            context["progress_list"] = ChallengeTracker.objects.filter(student=request.user.student)
            for challenge in context["challenges"]:
                completed_challenges = request.user.student.completed_challenge_questions.filter(challenge=challenge).count()
                challenges_count = challenge.question_set.count()
                context["completed_challenges"].append(completed_challenges)
                context["challenges_count"].append(challenges_count)
                context["completed_challenges_percentage"].append(ChallengeTracker.objects.get(challenge=challenge, student=request.user.student))
            return context
        if category == "health":
            context["bmi"] = user_data.weight / (user_data.height * 0.308 * user_data.height * 0.308)
            context["weight_health"] = get_health_from_bmi(context["bmi"])
            return context
        # if category == "quizzes":
        #     context["quiz_list"] = get_quiz(user_data.grade)
        if category == "challenges":
            context["challenges"] = get_challenges(user_data.grade)
            context["progress_list"] = ChallengeTracker.objects.filter(student=request.user.student)
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
                child_data["challenges"] = get_challenges(student.grade)
                child_data["completed_challenges"] = []
                child_data["challenges_count"] = []
                child_data["completed_challenges_percentage"] = []
                child_data["progress_list"] = ChallengeTracker.objects.filter(student=student)
                children_data.append(child_data)
            context = {
                "children_data": children_data,
            }
    elif user_type == "teacher":
        user_data = request.user.teacher.grade.student_set.all()
        students_data = []
        for student in user_data:
            student_data = {}
            student_data["user_data"] = student
            student_data["weight_health"] = get_health_from_bmi(student.bmi())
            student_data["attendance"] = Attendence.objects.get(student_id=student.id)
            student_data["required_xp"] = next_level(student.level)
            student_data["xp_progress"] = (int(student.xp) / student_data["required_xp"]) * 100;
            student_data["progress_list"] = ChallengeTracker.objects.filter(student=student)
            students_data.append(student_data)
        context = {
            "students_data": students_data,
        }

    if category == "leaderboard" or "dashboard":
        context["leaderboard"] = leaderboard

    return context