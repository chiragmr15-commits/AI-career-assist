from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import MoodEntry, EmotionAnalysis, MoodTrend, MotivationalTip, ProductivitySuggestion
from .serializers import MoodEntrySerializer, MoodTrendSerializer, MotivationalTipSerializer
from utils.nlp_processor import EmotionAnalyzer
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404

class AddMoodEntryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        journal_entry = request.data.get('journal_entry', '')
        mood = request.data.get('mood', 'Neutral')
        stress_level = request.data.get('stress_level', 'Moderate')
        energy_level = request.data.get('energy_level', 5)

        entry = MoodEntry.objects.create(
            user=request.user,
            journal_entry=journal_entry,
            mood=mood,
            stress_level=stress_level,
            energy_level=energy_level
        )

        # Analyze emotion
        analyzer = EmotionAnalyzer()
        emotion_data = analyzer.analyze_emotion(journal_entry)

        entry.anxiety_score = emotion_data.get('anxiety', 0)
        entry.motivation_score = emotion_data.get('motivation', 0)
        entry.save()

        analysis = EmotionAnalysis.objects.create(
            mood_entry=entry,
            detected_emotions=emotion_data.get('emotions', []),
            sentiment_score=emotion_data.get('sentiment', 0),
            dominant_emotion=emotion_data.get('dominant_emotion', ''),
            keywords=emotion_data.get('keywords', [])
        )

        # Generate suggestions
        suggestions = analyzer.generate_productivity_suggestions(emotion_data)
        for suggestion in suggestions:
            ProductivitySuggestion.objects.create(
                mood_entry=entry,
                suggestion=suggestion['text'],
                category=suggestion['category'],
                priority=suggestion['priority']
            )

        return Response(MoodEntrySerializer(entry).data, status=status.HTTP_201_CREATED)

class MoodHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        entries = MoodEntry.objects.filter(user=request.user, created_at__gte=start_date)
        serializer = MoodEntrySerializer(entries, many=True)
        return Response(serializer.data)

class MoodTrendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get last 7 days of data
        week_ago = timezone.now() - timedelta(days=7)
        entries = MoodEntry.objects.filter(user=request.user, created_at__gte=week_ago)

        # Calculate averages
        mood_values = {'Very Happy': 5, 'Happy': 4, 'Neutral': 3, 'Sad': 2, 'Very Sad': 1}
        stress_values = {'Low': 1, 'Moderate': 2, 'High': 3, 'Very High': 4}

        avg_mood = sum(mood_values.get(e.mood, 3) for e in entries) / entries.count() if entries.count() > 0 else 0
        avg_stress = sum(stress_values.get(e.stress_level, 2) for e in entries) / entries.count() if entries.count() > 0 else 0
        avg_anxiety = entries.aggregate(Avg('anxiety_score'))['anxiety_score__avg'] or 0
        avg_motivation = entries.aggregate(Avg('motivation_score'))['motivation_score__avg'] or 0

        # Determine trend
        if entries.count() >= 2:
            latest_mood = mood_values.get(entries.first().mood, 3)
            oldest_mood = mood_values.get(entries.last().mood, 3)
            trend_direction = 'improving' if latest_mood > oldest_mood else 'declining' if latest_mood < oldest_mood else 'stable'
        else:
            trend_direction = 'stable'

        mood_trend, created = MoodTrend.objects.get_or_create(user=request.user)
        mood_trend.weekly_average_mood = avg_mood
        mood_trend.weekly_average_stress = avg_stress
        mood_trend.weekly_average_anxiety = avg_anxiety
        mood_trend.weekly_average_motivation = avg_motivation
        mood_trend.trend_direction = trend_direction
        mood_trend.save()

        serializer = MoodTrendSerializer(mood_trend)
        return Response(serializer.data)

class MotivationalTipsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recent_entry = MoodEntry.objects.filter(user=request.user).first()
        
        if recent_entry and recent_entry.analysis:
            dominant_emotion = recent_entry.analysis.dominant_emotion
            tips = MotivationalTip.objects.filter(
                trigger_emotion=dominant_emotion,
                is_active=True
            )[:5]
        else:
            tips = MotivationalTip.objects.filter(is_active=True)[:5]

        serializer = MotivationalTipSerializer(tips, many=True)
        return Response(serializer.data)

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        week_ago = timezone.now() - timedelta(days=7)
        entries = MoodEntry.objects.filter(user=request.user, created_at__gte=week_ago)

        most_common_mood = entries.values('mood').annotate(count=Count('id')).order_by('-count').first() if entries.exists() else None
        
        stats = {
            'total_entries_this_week': entries.count(),
            'average_stress_level': entries.aggregate(Avg('anxiety_score'))['anxiety_score__avg'] or 0,
            'average_motivation': entries.aggregate(Avg('motivation_score'))['motivation_score__avg'] or 0,
            'most_common_mood': most_common_mood['mood'] if most_common_mood else 'N/A',
        }
        return Response(stats)
