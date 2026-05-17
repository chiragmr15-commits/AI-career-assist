from django.urls import path
from .views import (
    GenerateInterviewView, GetInterviewSessionView, SubmitAnswerView,
    CompleteInterviewView, InterviewHistoryView, InterviewTemplateView
)

urlpatterns = [
    path('generate/', GenerateInterviewView.as_view(), name='generate'),
    path('session/<int:session_id>/', GetInterviewSessionView.as_view(), name='session'),
    path('answer/<int:question_id>/', SubmitAnswerView.as_view(), name='answer'),
    path('complete/<int:session_id>/', CompleteInterviewView.as_view(), name='complete'),
    path('history/', InterviewHistoryView.as_view(), name='history'),
    path('templates/', InterviewTemplateView.as_view(), name='templates'),
]
