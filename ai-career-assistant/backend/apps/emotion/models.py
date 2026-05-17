from django.db import models
from django.contrib.auth.models import User

class MoodEntry(models.Model):
    MOOD_CHOICES = [
        ('Very Happy', 'Very Happy'),
        ('Happy', 'Happy'),
        ('Neutral', 'Neutral'),
        ('Sad', 'Sad'),
        ('Very Sad', 'Very Sad'),
    ]

    STRESS_LEVEL_CHOICES = [
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High'),
        ('Very High', 'Very High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_entries')
    journal_entry = models.TextField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    stress_level = models.CharField(max_length=20, choices=STRESS_LEVEL_CHOICES)
    anxiety_score = models.FloatField(default=0)
    motivation_score = models.FloatField(default=0)
    energy_level = models.IntegerField(default=5, help_text="1-10 scale")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood} ({self.created_at.date()})"

    class Meta:
        ordering = ['-created_at']

class EmotionAnalysis(models.Model):
    mood_entry = models.OneToOneField(MoodEntry, on_delete=models.CASCADE, related_name='analysis')
    detected_emotions = models.JSONField(default=list)
    sentiment_score = models.FloatField(default=0)
    dominant_emotion = models.CharField(max_length=100, blank=True)
    keywords = models.JSONField(default=list)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.mood_entry.user.username}"

class MoodTrend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mood_trend')
    weekly_average_mood = models.FloatField(default=0)
    weekly_average_stress = models.FloatField(default=0)
    weekly_average_anxiety = models.FloatField(default=0)
    weekly_average_motivation = models.FloatField(default=0)
    trend_direction = models.CharField(max_length=20, default='stable')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Mood Trend"

class MotivationalTip(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=100)
    trigger_emotion = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProductivitySuggestion(models.Model):
    mood_entry = models.ForeignKey(MoodEntry, on_delete=models.CASCADE, related_name='productivity_suggestions')
    suggestion = models.TextField()
    category = models.CharField(max_length=100)
    priority = models.CharField(
        max_length=20,
        choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')],
        default='Medium'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion for {self.mood_entry.user.username}"
