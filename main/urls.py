from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("<str:category>/", views.dashboard_view, name="dashboard_category"),
    path("challenges/<int:id>", views.challenge_view, name="challenge"),
    path("challenge-questions/<int:id>", views.challenge_question_view, name="challenge_question"),
    path("error", views.error_view, name="error"),
]
