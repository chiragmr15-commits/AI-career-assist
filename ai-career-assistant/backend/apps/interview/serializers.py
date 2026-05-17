from rest_framework import serializers
from .models import InterviewSession, InterviewQuestion, InterviewAnswer, InterviewTemplate

class InterviewAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewAnswer
        fields = ['confidence_score', 'clarity_score', 'technical_depth', 'overall_score', 'feedback', 'improvement_suggestions']

class InterviewQuestionSerializer(serializers.ModelSerializer):
    answer = InterviewAnswerSerializer(read_only=True)

    class Meta:
        model = InterviewQuestion
        fields = ['id', 'question_text', 'difficulty_level', 'category', 'suggested_answer', 'answer', 'order']

class InterviewSessionSerializer(serializers.ModelSerializer):
    questions = InterviewQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = InterviewSession
        fields = ['id', 'interview_type', 'job_role', 'company', 'started_at', 'completed_at', 'overall_score', 'is_completed', 'questions']

class InterviewTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewTemplate
        fields = ['id', 'name', 'template_type', 'description', 'difficulty_level', 'questions']

class SubmitAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewAnswer
        fields = ['user_answer']
