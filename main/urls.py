from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("<str:category>/", views.dashboard_category_view, name="dashboard_category"),
    path("error", views.error_view, name="error"),
]
