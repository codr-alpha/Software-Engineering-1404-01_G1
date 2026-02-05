from django.urls import path
from . import views

urlpatterns = [
    # API Endpoints
    path("api/submit-writing/", views.submit_writing, name="submit_writing"),
    
    # HTML Views (Front-end will use these later)
    path("", views.base, name="team7_index"),
    path("ping/", views.ping, name="team7_ping"),
]