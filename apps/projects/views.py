# apps/projects/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, ProjectVersion
from .forms import ProjectStep1Form, ProjectStep2Form


def projects_home(request):
    """صفحه‌ی اصلی مدیریت پروژه‌ها."""
    return render(request, 'projects/home.html')

def project_list(request):
    """نمایش فهرست پروژه‌ها."""
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_detail(request, pk):
    """نمای جزئیات یک پروژه خاص."""
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})

def create_project_step1(request):
    """گام اول ایجاد پروژه: اطلاعات اولیه."""
    if request.method == 'POST':
        form = ProjectStep1Form(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('create_project_step2', pk=project.pk)
    else:
        form = ProjectStep1Form()
    return render(request, 'projects/create_step1.html', {'form': form})

def create_project_step2(request, pk):
    """گام دوم ایجاد پروژه: نوع کسب‌وکار."""
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectStep2Form(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectStep2Form(instance=project)
    return render(request, 'projects/create_step2.html', {'form': form})


# apps/projects/views.py

from django.shortcuts import render

def projects_home(request):
    """صفحه‌ی اصلی مدیریت پروژه‌ها."""
    return render(request, 'projects/home.html')

"""
ویوهای مربوط به مدیریت پروژه‌ها و جداول پویا
"""

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db import transaction
import json

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    Project, ProjectChapter, DynamicTable, TableColumn, 
    TableRow, CellValue, CalculationFormula, CalculationCache
)
from .services import CalculationEngine, TableManager
from .serializers import (
    ProjectSerializer, ProjectChapterSerializer, DynamicTableSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    """API برای مدیریت پروژه‌ها"""
    
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    
    @action(detail=True, methods=['get'])
    def chapters(self, request, pk=None):
        """دریافت فصول یک پروژه"""
        project = self.get_object()
        chapters = project.chapters.all().order_by('order')
        serializer = ProjectChapterSerializer(chapters, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def create_chapter(self, request, pk=None):
        """ایجاد فصل جدید"""
        project = self.get_object()
        table_manager = TableManager(project)
        
        title = request.data.get('title')
        order = request.data.get('order', 1)
        description = request.data.get('description', '')
        
        try:
            chapter = table_manager.create_chapter(title, order, description)
            serializer = ProjectChapterSerializer(chapter)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': f'خطا در ایجاد فصل: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def calculation_summary(self, request, pk=None):
        """خلاصه محاسبات پروژه"""
        project = self.get_object()
        calc_engine = CalculationEngine(project)
        
        summary = {
            'total_chapters': project.chapters.count(),
            'total_tables': sum(ch.tables.count() for ch in project.chapters.all()),
            'last_calculation': None,
            'cached_results': []
        }
        
        # نتایج کش شده
        cached_data = CalculationCache.objects.filter(project=project)
        summary['cached_results'] = [
            {
                'key': cache.cache_key,
                'value': cache.cached_value,
                'last_updated': cache.last_updated
            }
            for cache in cached_data
        ]
        
        return Response(summary)


class ChapterViewSet(viewsets.ModelViewSet):
    """API برای مدیریت فصول"""
    
    serializer_class = ProjectChapterSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ProjectChapter.objects.filter(project__owner=self.request.user)
    
    @action(detail=True, methods=['get'])
    def tables(self, request, pk=None):
        """دریافت جداول یک فصل"""
        chapter = self.get_object()
        tables = chapter.tables.all().order_by('order')
        serializer = DynamicTableSerializer(tables, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def create_table(self, request, pk=None):
        """ایجاد جدول جدید"""
        chapter = self.get_object()
        table_manager = TableManager(chapter.project)
        
        name = request.data.get('name')
        order = request.data.get('order', 1)
        
        try:
            table = table_manager.create_table(chapter, name, order)
            serializer = DynamicTableSerializer(table)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': f'خطا در ایجاد جدول: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TableViewSet(viewsets.ModelViewSet):
    """API برای مدیریت جداول"""
    
    serializer_class = DynamicTableSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DynamicTable.objects.filter(chapter__project__owner=self.request.user)
    
    @action(detail=True, methods=['get'])
    def data(self, request, pk=None):
        """دریافت داده‌های کامل جدول"""
        table = self.get_object()
        table_manager = TableManager(table.chapter.project)
        
        data = table_manager.get_table_data(table)
        return Response(data)
    
    @action(detail=True, methods=['post'])
    def add_column(self, request, pk=None):
        """اضافه کردن ستون جدید"""
        table = self.get_object()
        table_manager = TableManager(table.chapter.project)
        
        name = request.data.get('name')
        column_type = request.data.get('type', 'text')
        order = request.data.get('order', 1)
        unit = request.data.get('unit', '')
        formula = request.data.get('formula', '')
        
        try:
            column = table_manager.add_column(table, name, column_type, order, unit, formula)
            
            return Response({
                'id': column.id,
                'name': column.name,
                'type': column.column_type,
                'order': column.order,
                'unit': column.unit,
                'formula': column.formula
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': f'خطا در اضافه کردن ستون: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def add_row(self, request, pk=None):
        """اضافه کردن ردیف جدید"""
        table = self.get_object()
        table_manager = TableManager(table.chapter.project)
        
        label = request.data.get('label')
        order = request.data.get('order', 1)
        
        try:
            row = table_manager.add_row(table, label, order)
            
            return Response({
                'id': row.id,
                'label': row.label,
                'order': row.order
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': f'خطا در اضافه کردن ردیف: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def update_cell(self, request, pk=None):
        """به‌روزرسانی مقدار سلول"""
        table = self.get_object()
        table_manager = TableManager(table.chapter.project)
        
        row_id = request.data.get('row_id')
        column_id = request.data.get('column_id')
        value = request.data.get('value', '')
        
        try:
            row = TableRow.objects.get(id=row_id, table=table)
            column = TableColumn.objects.get(id=column_id, table=table)
            
            table_manager.update_cell_value(row, column, value)
            
            # دریافت مقدار به‌روزرسانی شده
            cell = CellValue.objects.get(row=row, column=column)
            final_value = cell.calculated_value if column.column_type in ['calculated', 'reference'] else cell.value
            
            return Response({
                'success': True,
                'value': final_value,
                'raw_value': cell.value
            })
        except Exception as e:
            return Response(
                {'error': f'خطا در به‌روزرسانی سلول: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])  
    def recalculate(self, request, pk=None):
        """محاسبه مجدد کل جدول"""
        table = self.get_object()
        calc_engine = CalculationEngine(table.chapter.project)
        
        try:
            calc_engine.recalculate_table(table)
            
            # دریافت داده‌های به‌روز
            table_manager = TableManager(table.chapter.project)
            updated_data = table_manager.get_table_data(table)
            
            return Response({
                'success': True,
                'message': 'جدول با موفقیت محاسبه مجدد شد',
                'data': updated_data
            })
        except Exception as e:
            return Response(
                {'error': f'خطا در محاسبه مجدد: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def realtime_update(request):
    """به‌روزرسانی بلادرنگ"""
    try:
        data = json.loads(request.body)
        
        project_id = data.get('project_id')
        table_id = data.get('table_id')
        row_id = data.get('row_id')
        column_id = data.get('column_id')
        value = data.get('value', '')
        
        # بررسی دسترسی
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        table = get_object_or_404(DynamicTable, id=table_id, chapter__project=project)
        row = get_object_or_404(TableRow, id=row_id, table=table)
        column = get_object_or_404(TableColumn, id=column_id, table=table)
        
        # به‌روزرسانی
        table_manager = TableManager(project)
        table_manager.update_cell_value(row, column, value)
        
        # دریافت تغییرات وابسته
        dependent_changes = []
        
        # پیدا کردن سلول‌های وابسته
        table_name = table.name
        column_name = column.name
        
        dependent_columns = TableColumn.objects.filter(
            table__chapter__project=project,
            column_type__in=['calculated', 'reference'],
            formula__icontains=f'[{table_name}.{column_name}]'
        )
        
        for dep_col in dependent_columns:
            for dep_row in dep_col.table.rows.all():
                dep_cell = CellValue.objects.filter(row=dep_row, column=dep_col).first()
                if dep_cell:
                    dependent_changes.append({
                        'table_id': dep_col.table.id,
                        'row_id': dep_row.id,
                        'column_id': dep_col.id,
                        'value': dep_cell.calculated_value,
                        'raw_value': dep_cell.value
                    })
        
        # مقدار به‌روز شده سلول فعلی
        current_cell = CellValue.objects.get(row=row, column=column)
        final_value = current_cell.calculated_value if column.column_type in ['calculated', 'reference'] else current_cell.value
        
        return JsonResponse({
            'success': True,
            'updated_value': final_value,
            'dependent_changes': dependent_changes
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def get_formula_suggestions(request):
    """پیشنهادات فرمول براساس جداول موجود"""
    try:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, id=project_id, owner=request.user)
        
        suggestions = []
        
        # پیشنهادات جداول و ستون‌ها
        for chapter in project.chapters.all():
            for table in chapter.tables.all():
                for column in table.columns.all():
                    if column.column_type == 'number':
                        suggestions.append({
                            'type': 'column_reference',
                            'syntax': f'[{table.name}.{column.name}]',
                            'description': f'ارجاع به ستون {column.name} در جدول {table.name}',
                            'chapter': chapter.title
                        })
                        
                        suggestions.append({
                            'type': 'column_sum',
                            'syntax': f'SUM[{table.name}.{column.name}]',
                            'description': f'مجموع ستون {column.name} در جدول {table.name}',
                            'chapter': chapter.title
                        })
        
        # پیشنهادات فرمول‌های رایج
        common_formulas = [
            {
                'type': 'arithmetic',
                'syntax': '[table.col1] * [table.col2]',
                'description': 'ضرب دو ستون'
            },
            {
                'type': 'arithmetic', 
                'syntax': '[table.col1] / [table.col2]',
                'description': 'تقسیم دو ستون'
            },
            {
                'type': 'arithmetic',
                'syntax': '([table.col1] + [table.col2]) * 0.1',
                'description': 'درصد از مجموع'
            }
        ]
        
        suggestions.extend(common_formulas)
        
        return JsonResponse({
            'suggestions': suggestions
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
