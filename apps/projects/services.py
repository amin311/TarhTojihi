"""
سرویس‌های محاسباتی پروژه
"""

import re
import json
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Any, Optional
from django.db import transaction
from django.db.models import Q
from django.core.cache import cache

from .models import (
    Project, ProjectChapter, DynamicTable, TableColumn, 
    TableRow, CellValue, CalculationFormula, CalculationCache
)


class CalculationEngine:
    """موتور محاسبات پویا"""
    
    def __init__(self, project: Project):
        self.project = project
        self.cache_timeout = 300  # 5 دقیقه
    
    def calculate_cell(self, cell: CellValue) -> Decimal:
        """محاسبه مقدار یک سلول"""
        column = cell.column
        
        if column.column_type == 'number':
            try:
                return Decimal(str(cell.value))
            except (InvalidOperation, ValueError):
                return Decimal('0')
        
        elif column.column_type == 'calculated':
            return self._evaluate_formula(column.formula, cell)
        
        elif column.column_type == 'reference':
            return self._resolve_reference(column.formula, cell)
        
        return Decimal('0')
    
    def _evaluate_formula(self, formula: str, context_cell: CellValue) -> Decimal:
        """ارزیابی فرمول محاسباتی"""
        if not formula:
            return Decimal('0')
        
        # جایگزینی متغیرها در فرمول
        processed_formula = self._substitute_variables(formula, context_cell)
        
        try:
            # امنیت: فقط عملیات ریاضی مجاز
            allowed_names = {
                "__builtins__": {},
                "abs": abs,
                "round": round,
                "min": min,
                "max": max,
                "sum": sum,
                "Decimal": Decimal,
            }
            
            result = eval(processed_formula, allowed_names)
            return Decimal(str(result))
        except Exception as e:
            print(f"خطا در محاسبه فرمول {formula}: {e}")
            return Decimal('0')
    
    def _substitute_variables(self, formula: str, context_cell: CellValue) -> str:
        """جایگزینی متغیرها در فرمول"""
        
        # الگوهای مختلف ارجاع:
        # [table.column] - ارجاع به ستون در همان ردیف
        # [table.column.row] - ارجاع به سلول مشخص
        # [chapter.table.column] - ارجاع به ستون در فصل دیگر
        # SUM[table.column] - مجموع ستون
        
        patterns = [
            # مجموع ستون
            (r'SUM\[([^.]+)\.([^.]+)\]', self._sum_column_reference),
            # ارجاع به سلول مشخص
            (r'\[([^.]+)\.([^.]+)\.([^.]+)\]', self._specific_cell_reference),
            # ارجاع به ستون در همان ردیف
            (r'\[([^.]+)\.([^.]+)\]', self._same_row_reference),
            # ارجاع بین فصول
            (r'\[([^.]+)\.([^.]+)\.([^.]+)\]', self._cross_chapter_reference),
        ]
        
        processed = formula
        for pattern, handler in patterns:
            matches = re.finditer(pattern, processed)
            for match in matches:
                try:
                    replacement = handler(match, context_cell)
                    processed = processed.replace(match.group(0), str(replacement))
                except Exception as e:
                    print(f"خطا در جایگزینی {match.group(0)}: {e}")
                    processed = processed.replace(match.group(0), '0')
        
        return processed
    
    def _sum_column_reference(self, match, context_cell: CellValue) -> Decimal:
        """محاسبه مجموع یک ستون"""
        table_name, column_name = match.groups()
        
        # پیدا کردن جدول و ستون
        table = DynamicTable.objects.filter(
            chapter__project=self.project,
            name=table_name
        ).first()
        
        if not table:
            return Decimal('0')
        
        column = table.columns.filter(name=column_name).first()
        if not column:
            return Decimal('0')
        
        # محاسبه مجموع تمام سلول‌های این ستون
        cells = CellValue.objects.filter(
            column=column
        ).exclude(id=context_cell.id)  # جلوگیری از ارجاع دایره‌ای
        
        total = Decimal('0')
        for cell in cells:
            total += self.calculate_cell(cell)
        
        return total
    
    def _same_row_reference(self, match, context_cell: CellValue) -> Decimal:
        """ارجاع به ستون دیگر در همان ردیف"""
        table_name, column_name = match.groups()
        
        # اگر جدول مشخص نشده، جدول فعلی را در نظر بگیر
        if table_name == 'this' or table_name == context_cell.column.table.name:
            target_column = context_cell.column.table.columns.filter(
                name=column_name
            ).first()
        else:
            table = DynamicTable.objects.filter(
                chapter__project=self.project,
                name=table_name
            ).first()
            if not table:
                return Decimal('0')
            
            target_column = table.columns.filter(name=column_name).first()
        
        if not target_column:
            return Decimal('0')
        
        # پیدا کردن سلول متناظر در همان ردیف
        target_cell = CellValue.objects.filter(
            row=context_cell.row,
            column=target_column
        ).first()
        
        if not target_cell:
            return Decimal('0')
        
        return self.calculate_cell(target_cell)
    
    def _specific_cell_reference(self, match, context_cell: CellValue) -> Decimal:
        """ارجاع به سلول مشخص"""
        table_name, column_name, row_name = match.groups()
        
        # پیدا کردن جدول
        table = DynamicTable.objects.filter(
            chapter__project=self.project,
            name=table_name
        ).first()
        
        if not table:
            return Decimal('0')
        
        # پیدا کردن ستون و ردیف
        column = table.columns.filter(name=column_name).first()
        row = table.rows.filter(label=row_name).first()
        
        if not column or not row:
            return Decimal('0')
        
        # پیدا کردن سلول
        cell = CellValue.objects.filter(row=row, column=column).first()
        if not cell:
            return Decimal('0')
        
        return self.calculate_cell(cell)
    
    def _cross_chapter_reference(self, match, context_cell: CellValue) -> Decimal:
        """ارجاع بین فصول"""
        chapter_name, table_name, column_name = match.groups()
        
        # پیدا کردن فصل
        chapter = ProjectChapter.objects.filter(
            project=self.project,
            title=chapter_name
        ).first()
        
        if not chapter:
            return Decimal('0')
        
        # پیدا کردن جدول
        table = chapter.tables.filter(name=table_name).first()
        if not table:
            return Decimal('0')
        
        # مجموع ستون را برگردان
        column = table.columns.filter(name=column_name).first()
        if not column:
            return Decimal('0')
        
        cells = CellValue.objects.filter(column=column)
        total = Decimal('0')
        for cell in cells:
            total += self.calculate_cell(cell)
        
        return total
    
    def recalculate_table(self, table: DynamicTable):
        """محاسبه مجدد کل جدول"""
        with transaction.atomic():
            # پیدا کردن تمام سلول‌های محاسباتی
            calculated_cells = CellValue.objects.filter(
                column__table=table,
                column__column_type__in=['calculated', 'reference']
            )
            
            for cell in calculated_cells:
                new_value = self.calculate_cell(cell)
                cell.calculated_value = new_value
                cell.save(update_fields=['calculated_value'])
    
    def recalculate_project(self):
        """محاسبه مجدد کل پروژه"""
        chapters = self.project.chapters.all().order_by('order')
        
        for chapter in chapters:
            tables = chapter.tables.all().order_by('order')
            for table in tables:
                self.recalculate_table(table)
    
    def get_cached_calculation(self, cache_key: str) -> Optional[Any]:
        """دریافت نتیجه محاسبه از کش"""
        cached_data = CalculationCache.objects.filter(
            project=self.project,
            cache_key=cache_key
        ).first()
        
        if cached_data:
            return cached_data.cached_value
        
        return None
    
    def set_cached_calculation(self, cache_key: str, value: Any):
        """ذخیره نتیجه محاسبه در کش"""
        CalculationCache.objects.update_or_create(
            project=self.project,
            cache_key=cache_key,
            defaults={'cached_value': value}
        )


class TableManager:
    """مدیریت جداول پویا"""
    
    def __init__(self, project: Project):
        self.project = project
        self.calc_engine = CalculationEngine(project)
    
    def create_chapter(self, title: str, order: int, description: str = "") -> ProjectChapter:
        """ایجاد فصل جدید"""
        return ProjectChapter.objects.create(
            project=self.project,
            title=title,
            order=order,
            description=description
        )
    
    def create_table(self, chapter: ProjectChapter, name: str, order: int) -> DynamicTable:
        """ایجاد جدول جدید"""
        return DynamicTable.objects.create(
            chapter=chapter,
            name=name,
            order=order
        )
    
    def add_column(self, table: DynamicTable, name: str, column_type: str, 
                   order: int, unit: str = "", formula: str = "") -> TableColumn:
        """اضافه کردن ستون به جدول"""
        return TableColumn.objects.create(
            table=table,
            name=name,
            column_type=column_type,
            order=order,
            unit=unit,
            formula=formula
        )
    
    def add_row(self, table: DynamicTable, label: str, order: int) -> TableRow:
        """اضافه کردن ردیف به جدول"""
        row = TableRow.objects.create(
            table=table,
            label=label,
            order=order
        )
        
        # ایجاد سلول‌های خالی برای تمام ستون‌ها
        for column in table.columns.all():
            CellValue.objects.create(
                row=row,
                column=column,
                value=""
            )
        
        return row
    
    def update_cell_value(self, row: TableRow, column: TableColumn, value: str):
        """به‌روزرسانی مقدار سلول"""
        with transaction.atomic():
            cell, created = CellValue.objects.get_or_create(
                row=row,
                column=column,
                defaults={'value': value}
            )
            
            if not created:
                cell.value = value
                cell.save()
            
            # محاسبه مجدد سلول
            if column.column_type in ['calculated', 'reference']:
                cell.calculated_value = self.calc_engine.calculate_cell(cell)
                cell.save(update_fields=['calculated_value'])
            
            # محاسبه مجدد سلول‌های وابسته
            self._recalculate_dependent_cells(cell)
    
    def _recalculate_dependent_cells(self, changed_cell: CellValue):
        """محاسبه مجدد سلول‌های وابسته"""
        # پیدا کردن فرمول‌هایی که به این سلول ارجاع دارند
        table_name = changed_cell.column.table.name
        column_name = changed_cell.column.name
        
        # جستجو در فرمول‌های مختلف
        dependent_columns = TableColumn.objects.filter(
            table__chapter__project=self.project,
            column_type__in=['calculated', 'reference'],
            formula__icontains=f'[{table_name}.{column_name}]'
        )
        
        for column in dependent_columns:
            cells = CellValue.objects.filter(column=column)
            for cell in cells:
                cell.calculated_value = self.calc_engine.calculate_cell(cell)
                cell.save(update_fields=['calculated_value'])
    
    def get_table_data(self, table: DynamicTable) -> Dict:
        """دریافت داده‌های کامل جدول"""
        rows_data = []
        
        for row in table.rows.all():
            row_data = {
                'id': row.id,
                'label': row.label,
                'order': row.order,
                'cells': {}
            }
            
            for cell in row.cells.all():
                column = cell.column
                cell_value = cell.calculated_value if column.column_type in ['calculated', 'reference'] else cell.value
                
                row_data['cells'][column.name] = {
                    'value': cell_value,
                    'raw_value': cell.value,
                    'type': column.column_type,
                    'unit': column.unit
                }
            
            rows_data.append(row_data)
        
        return {
            'table_id': table.id,
            'name': table.name,
            'columns': [
                {
                    'name': col.name,
                    'type': col.column_type,
                    'unit': col.unit,
                    'order': col.order
                }
                for col in table.columns.all()
            ],
            'rows': rows_data
        } 