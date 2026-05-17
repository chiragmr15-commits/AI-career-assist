from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import InterviewSession, InterviewQuestion, InterviewAnswer, InterviewTemplate
from .serializers import InterviewSessionSerializer, InterviewQuestionSerializer, InterviewTemplateSerializer, SubmitAnswerSerializer
from utils.nlp_processor import InterviewAnalyzer
from django.shortcuts import get_object_or_404
from django.utils import timezone
import random

class GenerateInterviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        interview_type = request.data.get('interview_type', 'Mixed')
        job_role = request.data.get('job_role', '')
        company = request.data.get('company', '')
        difficulty = request.data.get('difficulty', 'Medium')
        num_questions = request.data.get('num_questions', 5)

        session = InterviewSession.objects.create(
            user=request.user,
            interview_type=interview_type,
            job_role=job_role,
            company=company
        )

        analyzer = InterviewAnalyzer()
        questions = analyzer.generate_questions(
            interview_type=interview_type,
            job_role=job_role,
            difficulty=difficulty,
            count=num_questions
        )

        for idx, q in enumerate(questions):
            InterviewQuestion.objects.create(
                session=session,
                question_text=q['question'],
                difficulty_level=q.get('difficulty', 'Medium'),
                category=q.get('category', ''),
                suggested_answer=q.get('suggested_answer', ''),
                order=idx
            )

        return Response(InterviewSessionSerializer(session).data, status=status.HTTP_201_CREATED)

class GetInterviewSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
        serializer = InterviewSessionSerializer(session)
        return Response(serializer.data)

class SubmitAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, question_id):
        question = get_object_or_404(InterviewQuestion, id=question_id)
        
        if request.user != question.session.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        user_answer = request.data.get('answer', '')
        
        analyzer = InterviewAnalyzer()
        analysis = analyzer.analyze_answer(
            question=question.question_text,
            user_answer=user_answer,
            suggested_answer=question.suggested_answer,
            difficulty=question.difficulty_level
        )

        answer, created = InterviewAnswer.objects.get_or_create(question=question)
        answer.user_answer = user_answer
        answer.confidence_score = analysis['confidence']
        answer.clarity_score = analysis['clarity']
        answer.technical_depth = analysis['technical_depth']
        answer.overall_score = analysis['overall_score']
        answer.feedback = analysis['feedback']
        answer.improvement_suggestions = analysis['suggestions']
        answer.save()

        return Response(InterviewQuestionSerializer(question).data, status=status.HTTP_200_OK)

class CompleteInterviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
        
        # Calculate overall score
        answers = InterviewAnswer.objects.filter(question__session=session)
        if answers.exists():
            overall_score = sum(a.overall_score for a in answers) / answers.count()
            session.overall_score = overall_score
        
        session.is_completed = True
        session.completed_at = timezone.now()
        session.save()

        return Response(InterviewSessionSerializer(session).data, status=status.HTTP_200_OK)

class InterviewHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = InterviewSession.objects.filter(user=request.user)
        serializer = InterviewSessionSerializer(sessions, many=True)
        return Response(serializer.data)

class InterviewHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = InterviewSession.objects.filter(user=request.user).order_by('-started_at')
        serializer = InterviewSessionSerializer(sessions, many=True)
        return Response(serializer.data)

class InterviewTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        templates = InterviewTemplate.objects.all()
        serializer = InterviewTemplateSerializer(templates, many=True)
        return Response(serializer.data)
