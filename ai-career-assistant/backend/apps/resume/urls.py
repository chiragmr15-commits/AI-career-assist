from django.urls import path
from .views import (
    ResumeUploadView, AnalyzeResumeView, ResumeDetailView,
    AddSkillView, JobMatchingView
)

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='upload'),
    path('analyze/', AnalyzeResumeView.as_view(), name='analyze'),
    path('detail/', ResumeDetailView.as_view(), name='detail'),
    path('add-skill/', AddSkillView.as_view(), name='add-skill'),
    path('job-match/', JobMatchingView.as_view(), name='job-match'),
]
