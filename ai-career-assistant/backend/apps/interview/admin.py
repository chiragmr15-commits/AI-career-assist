from django.contrib import admin
from .models import InterviewSession, InterviewQuestion, InterviewAnswer, InterviewTemplate

@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'interview_type', 'job_role', 'overall_score', 'is_completed']
    search_fields = ['user__username', 'job_role']

@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'difficulty_level', 'category']
    search_fields = ['question_text', 'category']

@admin.register(InterviewAnswer)
class InterviewAnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'overall_score', 'answered_at']

@admin.register(InterviewTemplate)
class InterviewTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'difficulty_level']
    search_fields = ['name']
