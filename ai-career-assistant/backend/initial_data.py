import json

# Sample career paths data to load into database
CAREER_PATHS = [
    {
        'career': 'Software Engineer',
        'description': 'Develop, design, and maintain software applications',
        'required_skills': ['Python', 'Java', 'JavaScript', 'SQL', 'Git', 'REST API', 'Problem Solving'],
        'trending_skills': ['Python', 'Go', 'Rust', 'TypeScript', 'Cloud Computing'],
        'salary_range': '$80,000 - $200,000+',
        'job_outlook': 'Excellent (22% growth)',
        'average_experience_years': 5,
    },
    {
        'career': 'Data Analyst',
        'description': 'Analyze data and provide business insights',
        'required_skills': ['SQL', 'Python', 'Excel', 'Tableau', 'Statistics', 'Data Visualization'],
        'trending_skills': ['Python', 'SQL', 'Power BI', 'R', 'Machine Learning'],
        'salary_range': '$60,000 - $150,000+',
        'job_outlook': 'Excellent (36% growth)',
        'average_experience_years': 3,
    },
    {
        'career': 'AI/ML Engineer',
        'description': 'Develop AI and machine learning models',
        'required_skills': ['Python', 'TensorFlow', 'PyTorch', 'Machine Learning', 'Statistics', 'SQL'],
        'trending_skills': ['Python', 'TensorFlow', 'PyTorch', 'LLMs', 'Deep Learning'],
        'salary_range': '$100,000 - $250,000+',
        'job_outlook': 'Excellent (21% growth)',
        'average_experience_years': 4,
    },
    {
        'career': 'UI/UX Designer',
        'description': 'Design user interfaces and experiences',
        'required_skills': ['Figma', 'Adobe XD', 'UI Design', 'UX Research', 'Prototyping', 'Communication'],
        'trending_skills': ['Figma', 'Design Systems', 'Accessibility', 'Prototyping', 'User Research'],
        'salary_range': '$50,000 - $140,000+',
        'job_outlook': 'Good (13% growth)',
        'average_experience_years': 3,
    },
    {
        'career': 'DevOps Engineer',
        'description': 'Manage infrastructure and deployment pipelines',
        'required_skills': ['Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Linux', 'Git', 'Networking'],
        'trending_skills': ['Kubernetes', 'AWS', 'Terraform', 'GitHub Actions', 'ArgoCD'],
        'salary_range': '$90,000 - $210,000+',
        'job_outlook': 'Excellent (15% growth)',
        'average_experience_years': 5,
    },
]

MOTIVATIONAL_TIPS = [
    {
        'title': 'Take a Break',
        'content': 'When feeling overwhelmed, take a 10-minute break. Step outside, breathe deeply, and reset your mind.',
        'category': 'Wellness',
        'trigger_emotion': 'Stress',
    },
    {
        'title': 'Break Tasks Into Steps',
        'content': 'Large projects feel daunting. Break them into smaller, manageable tasks and celebrate each completion.',
        'category': 'Productivity',
        'trigger_emotion': 'Stress',
    },
    {
        'title': 'Practice Gratitude',
        'content': 'Write down 3 things you are grateful for today. This can shift your perspective and boost mood.',
        'category': 'Mental Health',
        'trigger_emotion': 'Sadness',
    },
    {
        'title': 'Exercise Regularly',
        'content': 'Physical activity releases endorphins, which improve mood and reduce stress. Even a 20-minute walk helps!',
        'category': 'Wellness',
        'trigger_emotion': 'Sadness',
    },
    {
        'title': 'Celebrate Small Wins',
        'content': 'Don\'t wait for big achievements. Celebrate every small victory along your journey.',
        'category': 'Motivation',
        'trigger_emotion': 'Low Motivation',
    },
    {
        'title': 'Connect with Others',
        'content': 'Reach out to friends or mentors. Social connection can boost motivation and provide valuable support.',
        'category': 'Social',
        'trigger_emotion': 'Loneliness',
    },
    {
        'title': 'Sleep Well',
        'content': 'Quality sleep is crucial for cognitive function. Aim for 7-9 hours each night.',
        'category': 'Wellness',
        'trigger_emotion': 'Fatigue',
    },
    {
        'title': 'Learn Something New',
        'content': 'Continue learning and growing. Take a course, read an article, or watch an educational video.',
        'category': 'Growth',
        'trigger_emotion': 'Curiosity',
    },
]

def load_data():
    """Load initial data into database"""
    from apps.career.models import CareerPath, MotivationalTip
    
    # Load career paths
    for path in CAREER_PATHS:
        CareerPath.objects.get_or_create(**path)
    
    # Load motivational tips
    for tip in MOTIVATIONAL_TIPS:
        MotivationalTip.objects.get_or_create(**tip)
    
    print("✅ Initial data loaded successfully!")

if __name__ == '__main__':
    import django
    django.setup()
    load_data()
