from django.urls import path
from . import views

urlpatterns = [
    path("", views.base),
    path("ping/", views.ping),
    path("lessons/", views.lessons_list_view, name="team2_lessons_list"),
]