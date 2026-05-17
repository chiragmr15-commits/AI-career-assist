from django.db import models
from django.contrib.auth.models import User

class CareerProfile(models.Model):
    CAREER_CHOICES = [
        ('Software Engineer', 'Software Engineer'),
        ('Data Analyst', 'Data Analyst'),
        ('AI/ML Engineer', 'AI/ML Engineer'),
        ('UI/UX Designer', 'UI/UX Designer'),
        ('Product Manager', 'Product Manager'),
        ('DevOps Engineer', 'DevOps Engineer'),
        ('Full Stack Developer', 'Full Stack Developer'),
        ('Backend Developer', 'Backend Developer'),
        ('Frontend Developer', 'Frontend Developer'),
        ('Mobile Developer', 'Mobile Developer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='career_profile')
    primary_career = models.CharField(max_length=100, choices=CAREER_CHOICES, blank=True)
    secondary_careers = models.JSONField(default=list)
    interests = models.JSONField(default=list)
    career_readiness_score = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Career Profile"

class CareerPath(models.Model):
    career = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    trending_skills = models.JSONField(default=list)
    salary_range = models.CharField(max_length=100)
    job_outlook = models.CharField(max_length=100)
    average_experience_years = models.IntegerField(default=0)

    def __str__(self):
        return self.career

class LearningResource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('Course', 'Course'),
        ('Tutorial', 'Tutorial'),
        ('Book', 'Book'),
        ('Project', 'Project'),
    ]

    career_path = models.ForeignKey(CareerPath, on_delete=models.CASCADE, related_name='learning_resources')
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPE_CHOICES)
    url = models.URLField()
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')],
        default='Beginner'
    )
    duration_hours = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    recommended_careers = models.JSONField(default=list)
    recommended_skills = models.JSONField(default=list)
    confidence_score = models.FloatField(default=0)
    reasoning = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendations for {self.user.username}"
