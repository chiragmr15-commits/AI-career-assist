from django.urls import path
from .views import (
    CareerRecommendationView, CareerPathView, CareerProfileView,
    SkillGapAnalysisView
)

urlpatterns = [
    path('recommendation/', CareerRecommendationView.as_view(), name='recommendation'),
    path('paths/', CareerPathView.as_view(), name='paths'),
    path('profile/', CareerProfileView.as_view(), name='profile'),
    path('skill-gap/', SkillGapAnalysisView.as_view(), name='skill-gap'),
]
