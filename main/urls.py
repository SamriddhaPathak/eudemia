from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("<str:category>/", views.dashboard_view, name="dashboard_category"),
    path("challenges/<int:id>", views.challenge_view, name="challenge"),
    path("challenge-questions/<int:id>", views.challenge_question_view, name="challenge_question"),
    path("health/<int:id>", views.health_edit_view, name="health-edit"),
    path("challenges/create/", views.challenge_create_view, name="challenge_create"),
    path("challenges/create/<int:challenge_id>/question", views.challenge_question_create_view, name="challenge_question_create"),
    path("error", views.error_view, name="error"),
]
