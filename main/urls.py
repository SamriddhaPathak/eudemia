from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("dashboard/<str:category>/", views.dashboard_category_view, name="dashboard_category"),
]
