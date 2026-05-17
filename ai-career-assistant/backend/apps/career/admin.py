from django.contrib import admin
from .models import CareerProfile, CareerPath, LearningResource, Recommendation

@admin.register(CareerProfile)
class CareerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'primary_career', 'career_readiness_score']
    search_fields = ['user__username', 'primary_career']

@admin.register(CareerPath)
class CareerPathAdmin(admin.ModelAdmin):
    list_display = ['career', 'salary_range', 'job_outlook']
    search_fields = ['career']

@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'career_path', 'resource_type', 'difficulty_level']
    search_fields = ['title', 'career_path__career']

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'confidence_score', 'created_at']
    search_fields = ['user__username']
