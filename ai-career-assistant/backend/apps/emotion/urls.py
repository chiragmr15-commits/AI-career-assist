from django.urls import path
from .views import (
    AddMoodEntryView, MoodHistoryView, MoodTrendView,
    MotivationalTipsView, DashboardStatsView
)

urlpatterns = [
    path('add/', AddMoodEntryView.as_view(), name='add'),
    path('history/', MoodHistoryView.as_view(), name='history'),
    path('trend/', MoodTrendView.as_view(), name='trend'),
    path('tips/', MotivationalTipsView.as_view(), name='tips'),
    path('stats/', DashboardStatsView.as_view(), name='stats'),
]
