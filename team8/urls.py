from django.urls import path

from . import views

urlpatterns = [
    path("", views.base),
    path("ping/", views.ping),
    path("wordcard/", views.WordCardView.as_view(), name="wordcard"),
    path('analysis/', views.analysis_views.as_view(), name='analysis_page'),
    path('api/reading-history/', analysis_views.api_get_history, name='api_history'),
    path('api/text-analysis/', analysis_views.api_perform_analysis, name='api_run_analysis'),
]