from django import forms
from django.contrib import messages
from .models import Student

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