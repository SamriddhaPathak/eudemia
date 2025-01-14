from .models import Challenge
from .models import Quiz
from .models import monthly_challenge
from django.contrib import admin

admin.site.register(Challenge)
admin.site.register(Quiz)
admin.site.register(monthly_challenge)