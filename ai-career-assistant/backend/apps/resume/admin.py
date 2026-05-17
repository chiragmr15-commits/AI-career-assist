from django.contrib import admin
from .models import Resume, Skill, Experience, Education, Project, AnalysisResult

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'ats_score', 'created_at']
    search_fields = ['user__username', 'full_name']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'proficiency', 'resume']
    search_fields = ['name']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'resume']
    search_fields = ['position', 'company']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'resume']
    search_fields = ['institution', 'degree']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'resume']
    search_fields = ['title']

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['resume', 'created_at']
    search_fields = ['resume__user__username']
