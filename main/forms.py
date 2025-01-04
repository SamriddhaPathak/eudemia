from django import forms
from django.contrib import messages

class LoginForm(forms.Form):
    usertype = forms.ChoiceField(
        widget = forms.RadioSelect(attrs={
            'class': 'form-control form-select',
        }),
        choices = [
            ('1', 'Teacher'),
            ('2', 'Student'),
            ('3', 'Parent'),
        ]
    )
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