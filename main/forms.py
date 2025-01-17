from django import forms
from django.contrib import messages
from .models import Challenge, QuizQuestion

class QuizForm(forms.ModelForm):