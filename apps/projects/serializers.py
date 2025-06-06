# apps/projects/serializers.py

"""
سریالایزرهای مربوط به پروژه‌ها و جداول پویا
"""

from rest_framework import serializers
from .models import (
    Project, ProjectVersion, ProjectChapter, DynamicTable, TableColumn, 
    TableRow, CellValue, CalculationFormula, CalculationCache
)


class ProjectSerializer(serializers.ModelSerializer):
    """سریالایزر پروژه"""
    
    chapters_count = serializers.SerializerMethodField()
    completion_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'business_type', 
            'created_at', 'updated_at', 'chapters_count', 'completion_percentage'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_chapters_count(self, obj):
        return obj.chapters.count()
    
    def get_completion_percentage(self, obj):
        # محاسبه درصد تکمیل براساس تعداد فصول و جداول
        total_chapters = obj.chapters.count()
        if total_chapters == 0:
            return 0
        
        completed_chapters = 0
        for chapter in obj.chapters.all():
            if chapter.tables.exists():
                completed_chapters += 1
        
        return int((completed_chapters / total_chapters) * 100)


class ProjectVersionSerializer(serializers.ModelSerializer):
    """سریالایزر نسخه‌های پروژه"""
    
    project_title = serializers.CharField(source='project.title', read_only=True)
    
    class Meta:
        model = ProjectVersion
        fields = [
            'id', 'project', 'project_title', 'version_number', 
            'data', 'created_at'
        ]
        read_only_fields = ['created_at']


class ProjectChapterSerializer(serializers.ModelSerializer):
    """سریالایزر فصل پروژه"""
    
    tables_count = serializers.SerializerMethodField()
    project_title = serializers.CharField(source='project.title', read_only=True)
    
    class Meta:
        model = ProjectChapter
        fields = [
            'id', 'title', 'order', 'description', 'project', 
            'project_title', 'tables_count'
        ]
    
    def get_tables_count(self, obj):
        return obj.tables.count()


class TableColumnSerializer(serializers.ModelSerializer):
    """سریالایزر ستون جدول"""
    
    class Meta:
        model = TableColumn
        fields = [
            'id', 'name', 'column_type', 'order', 'unit', 'formula'
        ]


class DynamicTableSerializer(serializers.ModelSerializer):
    """سریالایزر جدول پویا"""
    
    chapter_title = serializers.CharField(source='chapter.title', read_only=True)
    columns = TableColumnSerializer(many=True, read_only=True)
    columns_count = serializers.SerializerMethodField()
    rows_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DynamicTable
        fields = [
            'id', 'name', 'order', 'chapter', 'chapter_title',
            'columns', 'columns_count', 'rows_count'
        ]
    
    def get_columns_count(self, obj):
        return obj.columns.count()
    
    def get_rows_count(self, obj):
        return obj.rows.count()
