from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import LoginForm
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import password_validators_help_texts
from math import floor

# Create your views here.
@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')
    else:
        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)

def logout_view(request):
    logout(request)
    return redirect("index")

@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {
        "form": "",
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        fm  = PasswordChangeForm(user = request.user, data = request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            messages.success(request, "Your password has been changed succeccfully.")
            return redirect('dashboard')
    else: 
        fm = PasswordChangeForm(user = request.user)        
    return render(request, "users/change_password.html", {
        "form" : fm,
        "password_help_texts" : password_validators_help_texts(),
    })