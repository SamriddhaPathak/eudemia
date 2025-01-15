from .models import Subject
from .models import Challenge
from .models import Quiz
from .models import Question
from .models import Attendence
from django.contrib import admin

admin.site.register(Challenge)
admin.site.register(Quiz)
admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(Attendence)