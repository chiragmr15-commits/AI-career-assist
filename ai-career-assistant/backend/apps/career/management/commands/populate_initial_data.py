from django.core.management.base import BaseCommand
from django.db import transaction
from apps.interview.models import InterviewTemplate
from apps.emotion.models import MotivationalTip

class Command(BaseCommand):
    help = 'Populate initial data for interview templates and motivational tips'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating Interview Templates...")
        
        templates_data = [
            {
                'name': 'Software Engineer - Technical',
                'template_type': 'Technical',
                'description': 'Technical interview for Software Engineer position',
                'difficulty_level': 'Medium',
                'questions': [
                    "Explain the concept of object-oriented programming.",
                    "What is the difference between SQL and NoSQL databases?",
                    "Describe the MVC architecture pattern.",
                    "What are microservices and their advantages?",
                    "How do you optimize database queries?"
                ]
            },
            {
                'name': 'Software Engineer - HR',
                'template_type': 'HR',
                'description': 'Behavioral interview for Software Engineer position',
                'difficulty_level': 'Medium',
                'questions': [
                    "Tell me about yourself.",
                    "What are your strengths and weaknesses?",
                    "Why are you interested in this position?",
                    "How do you handle stress and pressure?",
                    "Describe a challenging project you worked on."
                ]
            },
            {
                'name': 'Data Analyst - Technical',
                'template_type': 'Technical',
                'description': 'Technical interview for Data Analyst position',
                'difficulty_level': 'Medium',
                'questions': [
                    "Explain SQL joins and their differences.",
                    "How would you approach data cleaning?",
                    "Describe how you would create a dashboard.",
                    "What is data normalization?",
                    "How do you handle missing data in your analysis?"
                ]
            }
        ]

        for template_data in templates_data:
            template, created = InterviewTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults={
                    'template_type': template_data['template_type'],
                    'description': template_data['description'],
                    'difficulty_level': template_data['difficulty_level'],
                    'questions': template_data['questions']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✓ Created template: {template.name}"))
            else:
                self.stdout.write(f"✗ Template already exists: {template.name}")

        self.stdout.write("Creating Motivational Tips...")
        
        tips_data = [
            {
                'title': 'You can do this!',
                'content': 'Remember that every expert was once a beginner. Keep pushing forward!',
                'category': 'Motivation',
                'trigger_emotion': 'Sadness'
            },
            {
                'title': 'Take a break',
                'content': 'Your brain needs rest. Take a 15-minute break, go for a walk, or meditate.',
                'category': 'Wellness',
                'trigger_emotion': 'Stress'
            },
            {
                'title': 'Celebrate small wins',
                'content': 'Every step forward counts! Celebrate the small victories along your journey.',
                'category': 'Motivation',
                'trigger_emotion': 'Neutral'
            },
            {
                'title': 'You are stronger than you think',
                'content': 'Challenges make you stronger. You have overcome difficult things before!',
                'category': 'Motivation',
                'trigger_emotion': 'Sadness'
            },
            {
                'title': 'Focus on progress, not perfection',
                'content': "Progress is progress. Don't let perfectionism hold you back.",
                'category': 'Productivity',
                'trigger_emotion': 'Stress'
            },
            {
                'title': 'You deserve rest',
                'content': 'Taking care of yourself is not selfish. Rest and recharge when needed.',
                'category': 'Wellness',
                'trigger_emotion': 'Very Sad'
            },
            {
                'title': 'Your skills are valuable',
                'content': 'You have unique skills and experiences. Trust in your abilities!',
                'category': 'Motivation',
                'trigger_emotion': 'Neutral'
            },
            {
                'title': 'Keep learning',
                'content': 'Every challenge is an opportunity to learn something new. Stay curious!',
                'category': 'Professional',
                'trigger_emotion': 'Neutral'
            },
        ]

        for tip_data in tips_data:
            tip, created = MotivationalTip.objects.get_or_create(
                title=tip_data['title'],
                defaults={
                    'content': tip_data['content'],
                    'category': tip_data['category'],
                    'trigger_emotion': tip_data['trigger_emotion'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✓ Created tip: {tip.title}"))
            else:
                self.stdout.write(f"✗ Tip already exists: {tip.title}")

        self.stdout.write(self.style.SUCCESS("\nData population complete!"))
