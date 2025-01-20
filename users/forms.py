from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-input',
            'placeholder': 'Username',
        }),
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-input',
            'placeholder': 'Password',
        }),
        label=''
    )

# Validator function to limit file size
def validate_image_size(value):
    max_size = 5 * 1024 * 1024  # 5 MB in bytes
    if value.size > max_size:
        raise ValidationError("The file size should not exceed 5 MB.")

class UserProfileForm(forms.Form):
    profile_picture = forms.ImageField(
        required=True,
        label="Profile Picture",
        validators=[validate_image_size]  # Add the validator here
    )