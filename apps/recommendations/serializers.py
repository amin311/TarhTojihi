# apps/recommendations/serializers.py

from rest_framework import serializers
from .models import Recommendation
from apps.projects.models import Project

class RecommendationSerializer(serializers.ModelSerializer):
    similar_projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())

    class Meta:
        model = Recommendation
        fields = ['id', 'project', 'similar_projects', 'score']
