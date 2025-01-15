from django.contrib.auth.models import User
from users.models import Class, Teacher, Student, Parent
from .models import Attendence
from math import floor

def get_user_data(request, *args):
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

    user_profile = model.objects.select_related("user").filter(user_id=request.user.id).values(*fields)[0]

    return user_profile

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
    leaderboard = Student.objects.select_related("user").values("user_id", "user__first_name", "user__last_name", "points", "level", "xp")
    leaderboard = sorted(leaderboard, key=lambda x: x["level"]+x["xp"], reverse=True)
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

def get_health_from_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"