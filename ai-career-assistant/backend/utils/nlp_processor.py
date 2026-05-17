import re
import json
from textblob import TextBlob
import PyPDF2
from docx import Document
from collections import Counter

class ResumeAnalyzer:
    def __init__(self):
        self.common_skills = [
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'Go', 'Rust', 'PHP', 'Ruby', 'Swift',
            'React', 'Angular', 'Vue.js', 'Django', 'Flask', 'Spring', 'ASP.NET', 'Express',
            'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Elasticsearch',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'CI/CD', 'Git', 'Linux',
            'Machine Learning', 'Data Science', 'AI', 'NLP', 'Computer Vision',
            'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum', 'Leadership',
            'Communication', 'Problem Solving', 'Teamwork', 'Project Management'
        ]

    def extract_text_from_file(self, file_path):
        """Extract text from PDF or DOCX"""
        try:
            if file_path.endswith('.pdf'):
                return self._extract_from_pdf(file_path)
            elif file_path.endswith('.docx'):
                return self._extract_from_docx(file_path)
            else:
                with open(file_path, 'r') as f:
                    return f.read()
        except Exception as e:
            return f"Error extracting text: {str(e)}"

    def _extract_from_pdf(self, file_path):
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except:
            pass
        return text

    def _extract_from_docx(self, file_path):
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except:
            pass
        return text

    def extract_contact_info(self, text):
        """Extract email and phone from resume text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'

        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)

        return {
            'email': emails[0] if emails else '',
            'phone': phones[0] if phones else ''
        }

    def extract_skills(self, text):
        """Extract skills from resume"""
        skills = []
        text_lower = text.lower()
        
        for skill in self.common_skills:
            if skill.lower() in text_lower:
                skills.append(skill)

        return list(set(skills))

    def calculate_ats_score(self, text, skills):
        """Calculate ATS (Applicant Tracking System) score"""
        score = 0
        max_score = 100

        # Check for contact info
        contact_info = self.extract_contact_info(text)
        if contact_info['email']:
            score += 10
        if contact_info['phone']:
            score += 10

        # Check for education keywords
        education_keywords = ['bachelor', 'master', 'phd', 'diploma', 'degree']
        if any(keyword in text.lower() for keyword in education_keywords):
            score += 15

        # Check for experience keywords
        if 'experience' in text.lower():
            score += 15

        # Check for skills
        score += min(len(skills) * 2, 30)

        # Check for projects
        if 'project' in text.lower():
            score += 10

        # Check for formatting (length indicates proper formatting)
        if len(text) > 500:
            score += 10

        return min(score, max_score)

    def analyze(self, file_path):
        """Full resume analysis"""
        text = self.extract_text_from_file(file_path)
        
        contact_info = self.extract_contact_info(text)
        skills = self.extract_skills(text)
        ats_score = self.calculate_ats_score(text, skills)

        # Extract name from text (usually at the beginning)
        lines = text.split('\n')
        name = lines[0] if lines else ''

        # Identify weak areas
        weak_areas = []
        if ats_score < 60:
            weak_areas.append('ATS score is low - improve formatting')
        if len(skills) < 5:
            weak_areas.append('Limited technical skills listed')
        if 'project' not in text.lower():
            weak_areas.append('No projects mentioned')

        # Generate suggestions
        suggestions = []
        if len(skills) < 10:
            suggestions.append('Add more relevant skills to expand your technical profile')
        if 'achievement' not in text.lower().lower() and 'accomplished' not in text.lower():
            suggestions.append('Include more quantifiable achievements and accomplishments')
        suggestions.append('Use industry-standard keywords relevant to target positions')

        return {
            'name': name.strip(),
            'email': contact_info['email'],
            'phone': contact_info['phone'],
            'summary': text[:500],
            'skills': skills,
            'ats_score': ats_score,
            'missing_skills': ['Cloud Computing', 'Containerization', 'DevOps'] if len(skills) < 8 else [],
            'weak_areas': weak_areas,
            'suggestions': suggestions,
            'score_breakdown': {
                'contact_info': 20 if contact_info['email'] and contact_info['phone'] else 10,
                'skills': min(len(skills) * 10, 30),
                'education': 20,
                'experience': 20,
            }
        }

    def calculate_job_match(self, resume, job_description):
        """Calculate match between resume and job description"""
        resume_skills = set(skill.name.lower() for skill in resume.skills.all())
        
        job_keywords = set(word.lower() for word in job_description.split() if len(word) > 3)
        
        matches = resume_skills.intersection(job_keywords)
        match_score = len(matches) / max(len(resume_skills), len(job_keywords)) if resume_skills else 0
        
        return min(match_score, 1.0)

    def get_matching_skills(self, resume, job_description):
        """Get skills that match the job description"""
        resume_skills = set(skill.name.lower() for skill in resume.skills.all())
        job_keywords = set(word.lower() for word in job_description.lower().split())
        
        return list(resume_skills.intersection(job_keywords))

    def get_missing_skills_for_job(self, resume, job_description):
        """Get skills needed but not in resume"""
        resume_skills = set(skill.name.lower() for skill in resume.skills.all())
        job_keywords = set(word.lower() for word in job_description.lower().split() if len(word) > 3)
        
        return list(job_keywords - resume_skills)[:10]


class InterviewAnalyzer:
    def __init__(self):
        self.technical_questions = [
            "Explain the concept of object-oriented programming.",
            "What is the difference between SQL and NoSQL databases?",
            "Describe the MVC architecture pattern.",
            "What are microservices and their advantages?",
            "How do you optimize database queries?",
            "Explain RESTful API design principles.",
            "What is machine learning and its types?",
            "Describe the difference between async and sync programming.",
        ]

        self.hr_questions = [
            "Tell me about yourself.",
            "What are your strengths and weaknesses?",
            "Why are you interested in this position?",
            "How do you handle stress and pressure?",
            "Describe a challenging project you worked on.",
            "How do you work in a team environment?",
            "What are your career goals?",
            "Tell me about a time you showed leadership.",
        ]

    def generate_questions(self, interview_type='Mixed', job_role='', difficulty='Medium', count=5):
        """Generate interview questions"""
        import random

        questions = []

        if interview_type in ['Technical', 'Mixed']:
            questions.extend(self.technical_questions[:count//2])

        if interview_type in ['HR', 'Behavioral', 'Mixed']:
            questions.extend(self.hr_questions[:count//2])

        questions = questions[:count]

        return [
            {
                'question': q,
                'difficulty': difficulty,
                'category': 'Technical' if q in self.technical_questions else 'HR',
                'suggested_answer': f'A comprehensive answer to: {q}'
            }
            for q in questions
        ]

    def analyze_answer(self, question, user_answer, suggested_answer='', difficulty='Medium'):
        """Analyze user's interview answer"""
        blob = TextBlob(user_answer)
        
        # Calculate confidence (based on length and sentiment)
        confidence = min(len(user_answer) / 500, 1.0)
        
        # Calculate clarity (using textblob polarity)
        clarity = max(0, (blob.sentiment.polarity + 1) / 2) * 100
        
        # Calculate technical depth (based on keywords)
        technical_keywords = ['algorithm', 'data structure', 'optimization', 'pattern', 'design', 'system']
        technical_depth = sum(1 for keyword in technical_keywords if keyword in user_answer.lower()) / len(technical_keywords) * 100
        
        # Overall score
        overall_score = (confidence * 30 + clarity * 40 + technical_depth * 30) / 100

        # Feedback
        feedback = "Good attempt. "
        if confidence < 0.5:
            feedback += "Try to provide more detailed answers. "
        if clarity < 50:
            feedback += "Work on clarity and structure. "
        if technical_depth < 40:
            feedback += "Add more technical depth to your answer. "

        # Suggestions
        suggestions = []
        if len(user_answer) < 100:
            suggestions.append("Provide more elaborate answers")
        if blob.sentiment.polarity < 0:
            suggestions.append("Maintain a positive tone")
        suggestions.append("Include specific examples from your experience")

        return {
            'confidence': confidence,
            'clarity': clarity,
            'technical_depth': technical_depth,
            'overall_score': overall_score,
            'feedback': feedback,
            'suggestions': suggestions
        }


class EmotionAnalyzer:
    def __init__(self):
        self.stress_keywords = ['stressed', 'overwhelmed', 'pressure', 'anxious', 'worried', 'tense']
        self.happiness_keywords = ['happy', 'excited', 'great', 'wonderful', 'perfect', 'amazing']
        self.sadness_keywords = ['sad', 'depressed', 'unhappy', 'down', 'miserable', 'awful']

    def analyze_emotion(self, text):
        """Analyze emotions in text"""
        blob = TextBlob(text)
        
        # Sentiment analysis (-1 to 1, convert to 0-1)
        sentiment = (blob.sentiment.polarity + 1) / 2
        
        # Detect emotions
        emotions = []
        anxiety = 0
        motivation = 0
        
        text_lower = text.lower()

        if any(keyword in text_lower for keyword in self.stress_keywords):
            emotions.append('Stress')
            anxiety = 0.7
        
        if any(keyword in text_lower for keyword in self.happiness_keywords):
            emotions.append('Joy')
            motivation = 0.8
        
        if any(keyword in text_lower for keyword in self.sadness_keywords):
            emotions.append('Sadness')
            motivation = 0.3

        # Map sentiment to anxiety (now sentiment is 0-1)
        if sentiment < 0.3:
            anxiety = max(anxiety, 0.8)
        elif sentiment > 0.7:
            anxiety = min(anxiety, 0.3)
        else:
            anxiety = max(anxiety, 0.5)

        # Dominant emotion
        dominant_emotion = emotions[0] if emotions else 'Neutral'

        # Extract keywords
        words = text.split()
        keywords = [word for word in words if len(word) > 4]

        return {
            'emotions': emotions,
            'sentiment': sentiment,
            'anxiety': anxiety,
            'motivation': motivation,
            'dominant_emotion': dominant_emotion,
            'keywords': keywords[:10]
        }

    def generate_productivity_suggestions(self, emotion_data):
        """Generate productivity suggestions based on emotions"""
        suggestions = []
        dominant = emotion_data.get('dominant_emotion', '')

        if 'Stress' in emotion_data.get('emotions', []):
            suggestions.append({
                'text': 'Take a 10-minute break and practice deep breathing',
                'category': 'Mental Health',
                'priority': 'High'
            })
            suggestions.append({
                'text': 'Break your tasks into smaller chunks',
                'category': 'Productivity',
                'priority': 'High'
            })

        if emotion_data.get('motivation', 0) < 0.5:
            suggestions.append({
                'text': 'Set one small achievable goal and celebrate when completed',
                'category': 'Motivation',
                'priority': 'High'
            })

        if emotion_data.get('anxiety', 0) > 0.6:
            suggestions.append({
                'text': 'Try meditation or yoga for 15 minutes',
                'category': 'Wellness',
                'priority': 'Medium'
            })

        suggestions.append({
            'text': 'Take a short walk to refresh your mind',
            'category': 'Wellness',
            'priority': 'Medium'
        })

        return suggestions
