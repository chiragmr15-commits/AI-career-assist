from django.contrib import admin
from .models import MoodEntry, EmotionAnalysis, MoodTrend, MotivationalTip, ProductivitySuggestion

@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'mood', 'stress_level', 'created_at']
    search_fields = ['user__username']
    date_hierarchy = 'created_at'

@admin.register(EmotionAnalysis)
class EmotionAnalysisAdmin(admin.ModelAdmin):
    list_display = ['mood_entry', 'dominant_emotion', 'sentiment_score']

@admin.register(MoodTrend)
class MoodTrendAdmin(admin.ModelAdmin):
    list_display = ['user', 'trend_direction', 'last_updated']

@admin.register(MotivationalTip)
class MotivationalTipAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'trigger_emotion', 'is_active']
    list_filter = ['category', 'is_active']

@admin.register(ProductivitySuggestion)
class ProductivitySuggestionAdmin(admin.ModelAdmin):
    list_display = ['mood_entry', 'category', 'priority']
