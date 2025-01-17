from .models import Subject
from .models import Challenge
from .models import QuizQuestion
from .models import Question
from .models import Attendence
from .models import Quiz
from django.contrib import admin
from .models import Quote

admin.site.register(Challenge)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(Subject)
admin.site.register(Attendence)
admin.site.register(Quote)
