from rest_framework import serializers
from .models import MoodEntry, EmotionAnalysis, MoodTrend, MotivationalTip, ProductivitySuggestion

class EmotionAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionAnalysis
        fields = ['detected_emotions', 'sentiment_score', 'dominant_emotion', 'keywords', 'analyzed_at']

class ProductivitySuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductivitySuggestion
        fields = ['id', 'suggestion', 'category', 'priority']

class MoodEntrySerializer(serializers.ModelSerializer):
    analysis = EmotionAnalysisSerializer(read_only=True)
    productivity_suggestions = ProductivitySuggestionSerializer(many=True, read_only=True)

    class Meta:
        model = MoodEntry
        fields = ['id', 'journal_entry', 'mood', 'stress_level', 'anxiety_score', 'motivation_score', 
                  'energy_level', 'created_at', 'analysis', 'productivity_suggestions']

class MoodTrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodTrend
        fields = ['weekly_average_mood', 'weekly_average_stress', 'weekly_average_anxiety', 
                  'weekly_average_motivation', 'trend_direction', 'last_updated']

class MotivationalTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotivationalTip
        fields = ['id', 'title', 'content', 'category', 'trigger_emotion']
