from django.db import models
from django.contrib.auth.models import User

class InterviewSession(models.Model):
    INTERVIEW_TYPE_CHOICES = [
        ('Technical', 'Technical'),
        ('HR', 'HR'),
        ('Behavioral', 'Behavioral'),
        ('Mixed', 'Mixed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_sessions')
    interview_type = models.CharField(max_length=50, choices=INTERVIEW_TYPE_CHOICES)
    job_role = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    overall_score = models.FloatField(default=0)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.interview_type} Interview"

    class Meta:
        ordering = ['-started_at']

class InterviewQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    category = models.CharField(max_length=100, blank=True)
    suggested_answer = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question_text[:50]

class InterviewAnswer(models.Model):
    question = models.OneToOneField(InterviewQuestion, on_delete=models.CASCADE, related_name='answer')
    user_answer = models.TextField()
    confidence_score = models.FloatField(default=0)
    clarity_score = models.FloatField(default=0)
    technical_depth = models.FloatField(default=0)
    overall_score = models.FloatField(default=0)
    feedback = models.TextField(blank=True)
    improvement_suggestions = models.JSONField(default=list)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question.question_text[:30]}"

class InterviewTemplate(models.Model):
    TEMPLATE_TYPE_CHOICES = [
        ('Technical', 'Technical'),
        ('HR', 'HR'),
        ('Behavioral', 'Behavioral'),
    ]

    name = models.CharField(max_length=255, unique=True)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPE_CHOICES)
    description = models.TextField()
    questions = models.JSONField(default=list)
    difficulty_level = models.CharField(max_length=20, default='Medium')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
