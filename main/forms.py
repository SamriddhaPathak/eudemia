from django import forms
from django.contrib import messages
from .models import Student
from .models import Challenge, Question

challenge_type_choices = [
    ("weekly", "Weekly"),
    ("daily", "Daily"),
]

challenge_subject_choices = [
    ("math", "Math"),
    ("science", "Science"),
    ("english", "English"),
    ("social_studies", "Social Studies"),
    ("other", "Other"),
]

class HealthEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["height", "weight", "blood_group"]
        widgets = {
            "height": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Height in feet",
            }),
            "weight": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Weight in kilograms",
            }),
            "blood_group": forms.Select(attrs={
                "class": "form-control",
            }),
        }

class ChallengeCreateForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ["subject", "name", "challenge_type"]
        widgets = {
            "subject": forms.Select(choices=challenge_subject_choices, attrs={
                "class": "form-control",
            }),
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Challenge Name",
            }),
            "challenge_type": forms.Select(choices=challenge_type_choices, attrs={
                "class": "form-control",
            }),
        }

class ChallengeQuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question", "answer", "unit"]
        widgets = {
            "question": forms.Textarea(attrs={
                "class": "form-control",
            }),
            "answer": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "unit": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Unit (e.g., kg, meters) (Optional)",
            })
        }