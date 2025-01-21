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
    path("challenge/edit/<int:id>", views.challenge_edit_view, name="challenge_edit"),
    path("challenges/create/<int:challenge_id>/question", views.challenge_question_create_view, name="challenge_question_create"),
    path("challenges/delete/<int:id>", views.challenge_delete_view, name="challenge_delete"),
    path("shop/purchase/<int:id>", views.purchase_view, name="purchase"),
    path("settings/change-profile-border", views.change_profile_border_view, name="change_profile_border"),
    path("error", views.error_view, name="error"),
]
