from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/", include("django.contrib.auth.urls")),
    path("dashboard", views.dashboard_view, name="dashboard"),
]
  