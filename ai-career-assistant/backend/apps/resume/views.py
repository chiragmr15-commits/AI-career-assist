from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Resume, Skill, Experience, Education, Project, AnalysisResult
from .serializers import ResumeSerializer, ResumeUploadSerializer, SkillSerializer
from utils.nlp_processor import ResumeAnalyzer
from django.shortcuts import get_object_or_404
import json

class ResumeUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ResumeUploadSerializer(data=request.FILES)
        if serializer.is_valid():
            resume = Resume.objects.filter(user=request.user).first()
            if resume:
                resume.file = serializer.validated_data['file']
                resume.save()
            else:
                resume = Resume.objects.create(user=request.user, file=serializer.validated_data['file'])
            
            return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnalyzeResumeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        resume = get_object_or_404(Resume, user=request.user)
        
        analyzer = ResumeAnalyzer()
        analysis_data = analyzer.analyze(resume.file.path)
        
        resume.full_name = analysis_data.get('name', '')
        resume.email = analysis_data.get('email', '')
        resume.phone = analysis_data.get('phone', '')
        resume.summary = analysis_data.get('summary', '')
        resume.ats_score = analysis_data.get('ats_score', 0)
        resume.save()

        # Clear existing skills, experiences, education, projects
        resume.skills.all().delete()
        resume.experiences.all().delete()
        resume.education.all().delete()
        resume.projects.all().delete()

        # Add skills
        for skill in analysis_data.get('skills', []):
            Skill.objects.create(resume=resume, name=skill)

        # Create or update analysis
        analysis, created = AnalysisResult.objects.get_or_create(resume=resume)
        analysis.missing_skills = analysis_data.get('missing_skills', [])
        analysis.weak_areas = analysis_data.get('weak_areas', [])
        analysis.suggestions = analysis_data.get('suggestions', [])
        analysis.score_breakdown = analysis_data.get('score_breakdown', {})
        analysis.save()

        return Response(ResumeSerializer(resume).data, status=status.HTTP_200_OK)

class ResumeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resume = get_object_or_404(Resume, user=request.user)
        serializer = ResumeSerializer(resume)
        return Response(serializer.data)

    def put(self, request):
        resume = get_object_or_404(Resume, user=request.user)
        resume.full_name = request.data.get('full_name', resume.full_name)
        resume.email = request.data.get('email', resume.email)
        resume.phone = request.data.get('phone', resume.phone)
        resume.summary = request.data.get('summary', resume.summary)
        resume.save()

        serializer = ResumeSerializer(resume)
        return Response(serializer.data)

class AddSkillView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        resume = get_object_or_404(Resume, user=request.user)
        skill = Skill.objects.create(
            resume=resume,
            name=request.data.get('name'),
            proficiency=request.data.get('proficiency', 'Intermediate'),
            experience_years=request.data.get('experience_years', 0)
        )
        return Response(SkillSerializer(skill).data, status=status.HTTP_201_CREATED)

class JobMatchingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        resume = get_object_or_404(Resume, user=request.user)
        job_description = request.data.get('job_description', '')
        
        analyzer = ResumeAnalyzer()
        match_score = analyzer.calculate_job_match(resume, job_description)
        
        return Response({
            'match_score': match_score,
            'match_percentage': f"{match_score * 100:.1f}%",
            'skills_match': analyzer.get_matching_skills(resume, job_description),
            'missing_skills_for_job': analyzer.get_missing_skills_for_job(resume, job_description)
        })
