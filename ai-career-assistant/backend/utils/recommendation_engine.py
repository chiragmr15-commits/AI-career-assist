class RecommendationEngine:
    def __init__(self):
        self.career_paths = {
            'Software Engineer': {
                'skills': ['Python', 'Java', 'JavaScript', 'C++', 'SQL', 'Git', 'REST API'],
                'trending': ['Python', 'Go', 'Rust', 'TypeScript'],
                'description': 'Develop software applications and systems',
            },
            'Data Analyst': {
                'skills': ['SQL', 'Python', 'Excel', 'Tableau', 'Power BI', 'Statistics'],
                'trending': ['Python', 'SQL', 'R', 'Power BI'],
                'description': 'Analyze data and provide business insights',
            },
            'AI/ML Engineer': {
                'skills': ['Python', 'TensorFlow', 'PyTorch', 'Machine Learning', 'Statistics', 'SQL'],
                'trending': ['Python', 'TensorFlow', 'PyTorch', 'LLMs'],
                'description': 'Develop AI and machine learning models',
            },
            'UI/UX Designer': {
                'skills': ['Figma', 'Adobe XD', 'UI Design', 'UX Research', 'Prototyping', 'CSS'],
                'trending': ['Figma', 'Design Systems', 'Accessibility'],
                'description': 'Design user interfaces and experiences',
            },
            'DevOps Engineer': {
                'skills': ['Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Linux', 'Git'],
                'trending': ['Kubernetes', 'AWS', 'Terraform', 'GitHub Actions'],
                'description': 'Manage infrastructure and deployment pipelines',
            },
        }

    def recommend_careers(self, resume, interests):
        """Recommend careers based on resume and interests"""
        if not resume:
            return {
                'careers': [],
                'skills': [],
                'confidence': 0,
                'reasoning': 'Upload a resume to get recommendations',
                'readiness_score': 0
            }

        user_skills = set(skill.name.lower() for skill in resume.skills.all())
        
        career_scores = {}

        for career, info in self.career_paths.items():
            required_skills = set(skill.lower() for skill in info['skills'])
            matches = user_skills.intersection(required_skills)
            
            # Calculate match percentage
            match_percentage = len(matches) / len(required_skills) if required_skills else 0
            
            # Boost score based on interests
            interest_boost = 0.1 if any(interest.lower() in career.lower() for interest in interests) else 0
            
            career_scores[career] = match_percentage + interest_boost

        # Sort careers by score
        sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
        recommended_careers = [career[0] for career in sorted_careers[:3]]
        
        # Get recommended skills (trending + missing)
        recommended_skills = []
        if recommended_careers:
            top_career = recommended_careers[0]
            trending = self.career_paths[top_career]['trending']
            recommended_skills = [skill for skill in trending if skill.lower() not in user_skills]

        # Calculate readiness
        readiness_score = sorted_careers[0][1] * 100 if sorted_careers else 0

        reasoning = f"Based on your skills and interests, you're well-suited for {', '.join(recommended_careers[:2] if len(recommended_careers) > 1 else recommended_careers)}."

        return {
            'careers': recommended_careers,
            'skills': recommended_skills,
            'confidence': sorted_careers[0][1] if sorted_careers else 0,
            'reasoning': reasoning,
            'readiness_score': readiness_score
        }

    def calculate_skill_gap(self, resume, target_career):
        """Calculate skill gap for a target career"""
        if target_career not in self.career_paths:
            return {}

        user_skills = set(skill.name.lower() for skill in resume.skills.all())
        required_skills = set(skill.lower() for skill in self.career_paths[target_career]['skills'])
        
        gap_skills = list(required_skills - user_skills)
        matching_skills = list(required_skills.intersection(user_skills))

        return {
            'current_skills': matching_skills,
            'gap_skills': gap_skills,
            'completion_percentage': len(matching_skills) / len(required_skills) * 100 if required_skills else 0
        }
