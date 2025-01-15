from django import forms
from django.contrib import messages
from django.contrib.auth.models import User

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