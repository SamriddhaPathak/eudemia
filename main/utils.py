from django.contrib.auth.models import User
from users.models import Class, Teacher, Student, Parent
from .models import Attendance, QuizQuestion, Question, Challenge, Subject, Quote, Quiz
from math import floor
from django.utils.timezone import localdate

import random

def get_user_data_all(*args):
    usertype = get_user_type(request)
    usertype_model_map = {
        "student": Student,
        "parent": Parent,
        "teacher": Teacher,
    }
    
    if usertype not in usertype_model_map:
        return {}
    model = usertype_model_map[usertype]

    user_fields = [f.name for f in User._meta.fields if not f.is_relation]
    model_fields = [f.name for f in model._meta.fields if not f.name == "user"] + ["user_id"]

    all_fields = [f'user__{field}' for field in user_fields] + model_fields
    fields = list(args)

    for field in args:
        if field not in all_fields:
            raise Exception(f"ERROR: Could not find field '{field}' in model '{model.__name__}'") # raise exception if field not found
    
    if not args:
        fields = all_fields
    user_profiles = model.objects.select_related("user").values(*fields)

    return user_profiles

def get_leaderboard():
    leaderboard = Student.objects.select_related("user").values("user_id", "user__first_name", "user__last_name", "points", "level", "xp").order_by("-level", "-xp")
    return leaderboard

# returns the usertype of the user as a string
def get_user_type(request):
    user = User.objects.get(id=request.user.id)

    if hasattr(user, "student"):
        return "student"
    if hasattr(user, "parent"):
        return "parent"
    if hasattr(user, "teacher"):
        return "teacher"
    return "unknown"

def next_level(level):
    base_xp = 20
    exponent = 1.5
    return floor(base_xp * (level ** exponent))

def grant_xp(student_id, xp):
    student = Student.objects.get(id=student_id)
    required_xp = next_level(student.level)
    student.xp += xp
    if student.xp >= required_xp:
        student.level += 1
        student.xp -= required_xp
    student.save()

def grant_points(student_id, points):
    student = Student.objects.get(id=student_id)
    student.points += points
    student.save()

def get_health_from_bmi(bmi):
    if bmi < 18.5:
        return "underweight"
    elif 18.5 <= bmi < 25:
        return "normal"
    elif 25 <= bmi < 30:
        return "overweight"
    else:
        return "obese"

# def get_quiz(grade):
#     quizzes = list(Quiz.objects.all())
#     for quiz in quizzes:
#         if not quiz.quizquestion_set.filter(grade=grade).exists():
#             quizzes.remove(quiz)
#     return quizzes

def get_challenges(grade):
    challenge_list = Challenge.objects.filter(grade=grade)
    return challenge_list

def get_challenge_questions(challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    question_list = Question.objects.filter(challenge=challenge)
    return question_list


def get_random_quote():
    quotes = Quote.objects.all()
    return random.choice(quotes)

def attendance_done(grade):
    students = Student.objects.filter(grade=grade)
    today = localdate()
    for student in students:
        attendance = Attendance.objects.filter(student=student, date__date=today)
        if not attendance.exists():
            return False
    return True