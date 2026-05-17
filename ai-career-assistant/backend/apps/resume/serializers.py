from rest_framework import serializers
from .models import Resume, Skill, Experience, Education, Project, AnalysisResult

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'proficiency', 'experience_years']

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'company', 'position', 'start_date', 'end_date', 'description', 'currently_working']

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'gpa', 'currently_studying']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'technologies', 'link', 'start_date', 'end_date']

class AnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = ['missing_skills', 'weak_areas', 'suggestions', 'score_breakdown', 'created_at']

class ResumeSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    education = EducationSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    analysis = AnalysisResultSerializer(read_only=True)

    class Meta:
        model = Resume
        fields = ['id', 'full_name', 'email', 'phone', 'summary', 'ats_score', 'skills', 'experiences', 'education', 'projects', 'analysis', 'created_at']

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['file']
