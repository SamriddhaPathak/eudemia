from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from users.models import Class, Teacher, Student, Parent, UserProfile
from django.http import HttpResponse
from .models import Attendance, Quiz, Challenge, QuizTracker, ChallengeTracker, Quote, ShopItem, Purchase
from .config import SIDEBAR_ITEMS, BMI_ICONS
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

    additional_context = get_context(request, category)
    if additional_context:
        context.update(additional_context)

    return render(request, template, context)

@login_required
def purchase_view(request, id):
    usertype = get_user_type(request)
    shop_item = get_object_or_404(ShopItem, id=id)

    if shop_item.id in Purchase.objects.filter(student_id=request.user.student.id).values_list("shop_item_id", flat=True):
        messages.error(request, "Item already owned")
        return redirect("dashboard_category", category="shop")
    if request.user.student.points < shop_item.cost:
        messages.error(request, "Insufficient points")
        return redirect("dashboard_category", category="shop")

    if request.method == "POST":
        if request.user.student.points >= shop_item.cost:
            request.user.student.points -= shop_item.cost
            request.user.student.save()
            Purchase.objects.create(student=request.user.student, shop_item=shop_item)
        else:
            messages.error(request, "Insufficient points to purchase this item.")
        return redirect("dashboard")

    context = {
        "sidebar_items": SIDEBAR_ITEMS.get(usertype), # list of sidebar categories + the path to the icons

        "user": request.user,
        "usertype": usertype,
        "selected": "shop", # the currently selected category
        "profile_pic": request.user.userprofile.profile_pic.url,
        "shop_item": ShopItem.objects.get(id=id),
    }
    return render(request, "main/student/shop_purchase.html", context)

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
def challenge_edit_view(request, id):
    usertype = "teacher"

    challenge = get_object_or_404(Challenge, id=id)
    if request.method == "POST":
        form = ChallengeCreateForm(request.POST, instance=challenge)
        if form.is_valid():
            challenge = form.save()
            messages.success(request, "Challenge changed successfully")
            return redirect("dashboard_category", category="challenges")
    else:
        form = ChallengeCreateForm(instance=challenge)

    context = {
        "sidebar_items": SIDEBAR_ITEMS.get(usertype), # list of sidebar categories + the path to the icons

        "user": request.user,
        "usertype": usertype,
        "selected": "challenges", # the currently selected category
        "profile_pic": request.user.userprofile.profile_pic.url,
        "challenge": challenge,
        "form": form,
    }
    return render(request, "main/teacher/edit_challenge.html", context)

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

@login_required
def change_profile_border_view(request):
    usertype = "student"
    profile = request.user.userprofile
    purchases = Purchase.objects.filter(student_id=request.user.student.id)

    if request.method == "POST":
        item_id = request.POST.get("profile-border-id")
        item = ShopItem.objects.get(id=item_id) 
        user_profile = request.user.userprofile
        user_profile.profile_border = item
        user_profile.save()
        return redirect("dashboard")

    context = {
        "sidebar_items": SIDEBAR_ITEMS.get(usertype), # list of sidebar categories + the path to the icons

        "user": request.user,
        "usertype": usertype,
        "selected": "settings", # the currently selected category
        "profile_pic": request.user.userprofile.profile_pic.url,
        "profile": profile,
        "purchases": purchases,
    }
    return render(request, "main/student/change_profile_border.html", context)

@login_required
def update_attendance_view(request):
    usertype = "teacher"
    students = Student.objects.filter(grade=request.user.teacher.grade)

    if request.method == "POST":
        present = request.POST.getlist("present")
        print(present)
        for student in students:
            attendance = Attendance.objects.create(student=student)
            if str(student.id) in present:
                attendance.present = True
                student.grant_xp(10)
                student.grant_points(5)
            else:
                attendance.present = False
            attendance.save()
            if student.days_attended() % 10 == 0:
                student.grant_points(20)

    return redirect("dashboard_category", category="attendance")

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
            context["attendance"] = request.user.student.days_attended()
            context["challenges"] = get_challenges(user_data.grade)
            context["completed_challenges"] = []
            context["challenges_count"] = []
            context["completed_challenges_percentage"] = []
            context["progress_list"] = ChallengeTracker.objects.filter(student=request.user.student)
            for challenge in context["challenges"]:
                # completed_challenges = request.user.student.completed_challenge_questions.filter(challenge=challenge).count()
                challenges_count = challenge.question_set.count()
                # context["completed_challenges"].append(completed_challenges)
                context["challenges_count"].append(challenges_count)
                context["completed_challenges_percentage"].append(ChallengeTracker.objects.get(challenge=challenge, student=request.user.student))
            return context
        if category == "health":
            context["bmi"] = user_data.weight / (user_data.height * 0.308 * user_data.height * 0.308)
            context["weight_health"] = get_health_from_bmi(context["bmi"])
            context["bmi_icon"] = BMI_ICONS.get(context["weight_health"])
            return context
        # if category == "quizzes":
        #     context["quiz_list"] = get_quiz(user_data.grade)
        if category == "challenges":
            context["challenges"] = get_challenges(user_data.grade)
            context["progress_list"] = ChallengeTracker.objects.filter(student=request.user.student)
        if category == "shop":
            context["shop_items_avatars"] = ShopItem.objects.filter(item_type="avatar").order_by("-date_created")
            context["shop_items_borders"] = ShopItem.objects.filter(item_type="avatar_border").order_by("-date_created")
            context["purchases"] = Purchase.objects.filter(student=request.user.student).values_list("shop_item_id", flat=True)
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
                child_data["attendance"] = Attendance.objects.filter(student_id=student.id).values()[0]
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
                child_data["bmi_icon"] = BMI_ICONS.get(child_data["weight_health"])
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
        # user_data = request.user.teacher.grade.student_set.all()
        user_data = Student.objects.filter(grade=request.user.teacher.grade)
        students_data = []
        for student in user_data:
            student_data = {}
            student_data["user_data"] = student
            student_data["weight_health"] = get_health_from_bmi(student.bmi())
            student_data["bmi_icon"] = BMI_ICONS.get(student_data["weight_health"])
            student_data["required_xp"] = next_level(student.level)
            student_data["xp_progress"] = (int(student.xp) / student_data["required_xp"]) * 100;
            student_data["progress_list"] = ChallengeTracker.objects.filter(student=student)
            students_data.append(student_data)
        context = {
            "students_data": students_data,
            "attendance_list": Attendance.objects.filter(student_id__in=request.user.teacher.grade.student_set.values_list("id", flat=True)),
            "attendance_done": attendance_done(request.user.teacher.grade),
        }

    if category == "leaderboard" or "dashboard":
        context["leaderboard"] = leaderboard

    return context