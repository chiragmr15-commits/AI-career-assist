from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import CareerProfile, CareerPath, Recommendation
from .serializers import CareerProfileSerializer, CareerPathSerializer, RecommendationSerializer
from utils.recommendation_engine import RecommendationEngine
from django.shortcuts import get_object_or_404

class CareerRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        interests = request.data.get('interests', [])
        
        engine = RecommendationEngine()
        recommendations = engine.recommend_careers(None, interests)
        
        # Save recommendation
        rec, created = Recommendation.objects.get_or_create(user=request.user)
        rec.recommended_careers = recommendations['careers']
        rec.recommended_skills = recommendations['skills']
        rec.confidence_score = recommendations['confidence']
        rec.reasoning = recommendations['reasoning']
        rec.save()
        
        # Update or create career profile
        profile, created = CareerProfile.objects.get_or_create(user=request.user)
        if recommendations['careers']:
            profile.primary_career = recommendations['careers'][0]
            profile.secondary_careers = recommendations['careers'][1:]
            profile.interests = interests
            profile.career_readiness_score = recommendations['readiness_score']
            profile.save()
        
        return Response(RecommendationSerializer(rec).data, status=status.HTTP_200_OK)

class CareerPathView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        career_name = request.query_params.get('career', '')
        if career_name:
            career = get_object_or_404(CareerPath, career=career_name)
            serializer = CareerPathSerializer(career)
            return Response(serializer.data)
        
        careers = CareerPath.objects.all()
        serializer = CareerPathSerializer(careers, many=True)
        return Response(serializer.data)

class CareerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = CareerProfile.objects.get_or_create(user=request.user)
        serializer = CareerProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile, created = CareerProfile.objects.get_or_create(user=request.user)
        profile.primary_career = request.data.get('primary_career', profile.primary_career)
        profile.secondary_careers = request.data.get('secondary_careers', profile.secondary_careers)
        profile.interests = request.data.get('interests', profile.interests)
        profile.save()
        
        serializer = CareerProfileSerializer(profile)
        return Response(serializer.data)

class SkillGapAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resume = get_object_or_404(Resume, user=request.user)
        profile = get_object_or_404(CareerProfile, user=request.user)
        
        if not profile.primary_career:
            return Response({'error': 'No primary career set'}, status=status.HTTP_400_BAD_REQUEST)
        
        career = get_object_or_404(CareerPath, career=profile.primary_career)
        
        user_skills = [skill.name.lower() for skill in resume.skills.all()]
        required_skills = [skill.lower() for skill in career.required_skills]
        
        gap_skills = [skill for skill in required_skills if skill not in user_skills]
        
        return Response({
            'current_skills': user_skills,
            'required_skills': required_skills,
            'skill_gap': gap_skills,
            'completion_percentage': (len(user_skills) / len(required_skills) * 100) if required_skills else 0
        })
