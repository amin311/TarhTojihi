# apps/projects/serializers.py

from rest_framework import serializers
from .models import Project, ProjectVersion

class ProjectVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectVersion
        fields = ['id', 'version_number', 'data', 'created_at']

class ProjectSerializer(serializers.ModelSerializer):
    versions = ProjectVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'business_type', 'owner', 'created_at', 'updated_at', 'versions']
