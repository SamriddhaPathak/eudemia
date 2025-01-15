from django.contrib import admin
from .models import Student
from .models import Teacher
from .models import Parent
from .models import Class
from .models import UserProfile
# Register your models here.

admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Parent)
admin.site.register(UserProfile)