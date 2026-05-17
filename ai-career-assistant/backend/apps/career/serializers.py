from rest_framework import serializers
from .models import CareerProfile, CareerPath, LearningResource, Recommendation

class LearningResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningResource
        fields = ['id', 'title', 'resource_type', 'url', 'difficulty_level', 'duration_hours', 'description']

class CareerPathSerializer(serializers.ModelSerializer):
    learning_resources = LearningResourceSerializer(many=True, read_only=True)

    class Meta:
        model = CareerPath
        fields = ['id', 'career', 'description', 'required_skills', 'trending_skills', 
                  'salary_range', 'job_outlook', 'average_experience_years', 'learning_resources']

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ['id', 'recommended_careers', 'recommended_skills', 'confidence_score', 'reasoning', 'created_at']

class CareerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerProfile
        fields = ['id', 'primary_career', 'secondary_careers', 'interests', 'career_readiness_score', 'last_updated']
