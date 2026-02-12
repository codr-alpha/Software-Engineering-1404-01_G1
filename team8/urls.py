from django.urls import path
from django.views.generic import RedirectView  # <--- 1. Add this import

from . import views
from .views import analysis_views

# Make sure you are importing the Class correctly (as we discussed before)
from .views.wordcard import WordCardView 

urlpatterns = [
    # 2. CHANGE THIS LINE:
    # Instead of views.base, use RedirectView to send users to 'wordcard/'
    path("", RedirectView.as_view(url="wordcard/", permanent=False), name="index"),

    path("ping/", views.ping),
    
    # This remains the same
    path("wordcard/", WordCardView.as_view(), name="wordcard"),
    
    path('analysis/', analysis_views.text_analysis_page, name='analysis_page'),
    path('api/reading-history/', analysis_views.api_get_history, name='api_history'),
    path('api/text-analysis/', analysis_views.api_perform_analysis, name='api_run_analysis'),
]