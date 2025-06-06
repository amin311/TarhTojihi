"""
مثال عملی ایجاد پروژه با جداول پویا و محاسبات بین‌جدولی
"""

import os
import sys
import django

# تنظیم Django
sys.path.append('/d:/Gpt engeeneir/TarhTojihi')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feasibility_project.settings')
django.setup()

from apps.projects.models import Project, ProjectChapter, DynamicTable, TableColumn, TableRow, CellValue
from apps.projects.services import TableManager, CalculationEngine
from apps.users.models import User
from apps.categories.models import Category


def create_sample_project():
    """ایجاد پروژه نمونه"""
    
    # ایجاد کاربر (در صورت عدم وجود)
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@example.com'}
    )
    
    # ایجاد دسته‌بندی (در صورت عدم وجود)
    category, created = Category.objects.get_or_create(
        name='صنعتی',
        defaults={'description': 'پروژه‌های صنعتی'}
    )
    
    # ایجاد پروژه
    project = Project.objects.create(
        title='کارخانه تولید فولاد',
        description='پروژه احداث کارخانه تولید فولاد با ظرفیت ۱۰۰ هزار تن در سال',
        business_type=category,
        owner=user
    )
    
    print(f"پروژه '{project.title}' ایجاد شد.")
    
    # ایجاد مدیر جداول
    table_manager = TableManager(project)
    
    # فصل ۱: سرمایه‌گذاری ثابت
    chapter1 = table_manager.create_chapter(
        title='سرمایه‌گذاری ثابت',
        order=1,
        description='هزینه‌های سرمایه‌گذاری اولیه'
    )
    
    # جدول زمین و ساختمان
    land_table = table_manager.create_table(chapter1, 'زمین و ساختمان', 1)
    
    # ستون‌های جدول زمین
    table_manager.add_column(land_table, 'شرح', 'text', 1)
    table_manager.add_column(land_table, 'متراژ', 'number', 2, 'مترمربع')
    table_manager.add_column(land_table, 'قیمت واحد', 'number', 3, 'ریال')
    table_manager.add_column(land_table, 'جمع کل', 'calculated', 4, 'ریال', '[this.متراژ] * [this.قیمت واحد]')
    
    # ردیف‌های جدول زمین
    row1 = table_manager.add_row(land_table, 'خرید زمین', 1)
    row2 = table_manager.add_row(land_table, 'ساختمان کارخانه', 2)
    row3 = table_manager.add_row(land_table, 'ساختمان اداری', 3)
    
    # وارد کردن داده‌ها
    table_manager.update_cell_value(row1, land_table.columns.get(name='متراژ'), '10000')
    table_manager.update_cell_value(row1, land_table.columns.get(name='قیمت واحد'), '500000')
    
    table_manager.update_cell_value(row2, land_table.columns.get(name='متراژ'), '5000')
    table_manager.update_cell_value(row2, land_table.columns.get(name='قیمت واحد'), '2000000')
    
    table_manager.update_cell_value(row3, land_table.columns.get(name='متراژ'), '1000')
    table_manager.update_cell_value(row3, land_table.columns.get(name='قیمت واحد'), '3000000')
    
    print("جدول 'زمین و ساختمان' ایجاد شد.")
    
    # جدول ماشین‌آلات
    machinery_table = table_manager.create_table(chapter1, 'ماشین‌آلات', 2)
    
    # ستون‌های جدول ماشین‌آلات
    table_manager.add_column(machinery_table, 'شرح', 'text', 1)
    table_manager.add_column(machinery_table, 'تعداد', 'number', 2, 'عدد')
    table_manager.add_column(machinery_table, 'قیمت واحد', 'number', 3, 'ریال')
    table_manager.add_column(machinery_table, 'جمع کل', 'calculated', 4, 'ریال', '[this.تعداد] * [this.قیمت واحد]')
    
    # ردیف‌های ماشین‌آلات
    mach_row1 = table_manager.add_row(machinery_table, 'کوره ذوب', 1)
    mach_row2 = table_manager.add_row(machinery_table, 'دستگاه نورد', 2)
    mach_row3 = table_manager.add_row(machinery_table, 'جرثقیل', 3)
    
    # داده‌های ماشین‌آلات
    table_manager.update_cell_value(mach_row1, machinery_table.columns.get(name='تعداد'), '2')
    table_manager.update_cell_value(mach_row1, machinery_table.columns.get(name='قیمت واحد'), '50000000000')
    
    table_manager.update_cell_value(mach_row2, machinery_table.columns.get(name='تعداد'), '3')
    table_manager.update_cell_value(mach_row2, machinery_table.columns.get(name='قیمت واحد'), '30000000000')
    
    table_manager.update_cell_value(mach_row3, machinery_table.columns.get(name='تعداد'), '1')
    table_manager.update_cell_value(mach_row3, machinery_table.columns.get(name='قیمت واحد'), '5000000000')
    
    print("جدول 'ماشین‌آلات' ایجاد شد.")
    
    # جدول خلاصه سرمایه‌گذاری ثابت
    summary_table = table_manager.create_table(chapter1, 'خلاصه سرمایه‌گذاری', 3)
    
    # ستون‌های خلاصه
    table_manager.add_column(summary_table, 'بخش', 'text', 1)
    table_manager.add_column(summary_table, 'مبلغ', 'reference', 2, 'ریال', 'SUM[زمین و ساختمان.جمع کل]')
    
    # ردیف‌های خلاصه
    sum_row1 = table_manager.add_row(summary_table, 'زمین و ساختمان', 1)
    sum_row2 = table_manager.add_row(summary_table, 'ماشین‌آلات', 2)
    sum_row3 = table_manager.add_row(summary_table, 'جمع کل', 3)
    
    # تنظیم فرمول‌های ارجاع
    summary_machinery_col = summary_table.columns.get(name='مبلغ')
    summary_machinery_col.formula = 'SUM[ماشین‌آلات.جمع کل]'
    summary_machinery_col.save()
    
    # ردیف جمع کل
    table_manager.add_column(summary_table, 'جمع کل', 'calculated', 3, 'ریال', 'SUM[زمین و ساختمان.جمع کل] + SUM[ماشین‌آلات.جمع کل]')
    
    print("جدول 'خلاصه سرمایه‌گذاری' ایجاد شد.")
    
    # فصل ۲: سرمایه در گردش
    chapter2 = table_manager.create_chapter(
        title='سرمایه در گردش',
        order=2,
        description='هزینه‌های جاری و مواد اولیه'
    )
    
    # جدول مواد اولیه
    materials_table = table_manager.create_table(chapter2, 'مواد اولیه', 1)
    
    # ستون‌های مواد اولیه
    table_manager.add_column(materials_table, 'شرح', 'text', 1)
    table_manager.add_column(materials_table, 'مقدار ماهانه', 'number', 2, 'کیلوگرم')
    table_manager.add_column(materials_table, 'قیمت واحد', 'number', 3, 'ریال')
    table_manager.add_column(materials_table, 'هزینه ماهانه', 'calculated', 4, 'ریال', '[this.مقدار ماهانه] * [this.قیمت واحد]')
    table_manager.add_column(materials_table, 'هزینه سالانه', 'calculated', 5, 'ریال', '[this.هزینه ماهانه] * 12')
    
    # ردیف‌های مواد اولیه
    mat_row1 = table_manager.add_row(materials_table, 'سنگ آهن', 1)
    mat_row2 = table_manager.add_row(materials_table, 'زغال سنگ', 2)
    mat_row3 = table_manager.add_row(materials_table, 'سایر مواد', 3)
    
    # داده‌های مواد اولیه
    table_manager.update_cell_value(mat_row1, materials_table.columns.get(name='مقدار ماهانه'), '1000000')
    table_manager.update_cell_value(mat_row1, materials_table.columns.get(name='قیمت واحد'), '2000')
    
    table_manager.update_cell_value(mat_row2, materials_table.columns.get(name='مقدار ماهانه'), '500000')
    table_manager.update_cell_value(mat_row2, materials_table.columns.get(name='قیمت واحد'), '3000')
    
    table_manager.update_cell_value(mat_row3, materials_table.columns.get(name='مقدار ماهانه'), '100000')
    table_manager.update_cell_value(mat_row3, materials_table.columns.get(name='قیمت واحد'), '5000')
    
    print("جدول 'مواد اولیه' ایجاد شد.")
    
    # فصل ۳: خلاصه کل پروژه
    chapter3 = table_manager.create_chapter(
        title='خلاصه کل پروژه',
        order=3,
        description='خلاصه‌ای از کل هزینه‌های پروژه'
    )
    
    # جدول خلاصه نهایی
    final_table = table_manager.create_table(chapter3, 'خلاصه نهایی', 1)
    
    # ستون‌های خلاصه نهایی
    table_manager.add_column(final_table, 'بخش', 'text', 1)
    table_manager.add_column(final_table, 'مبلغ', 'reference', 2, 'ریال')
    
    # ردیف‌های خلاصه نهایی - استفاده از ارجاع بین فصول
    final_row1 = table_manager.add_row(final_table, 'سرمایه‌گذاری ثابت', 1)
    final_row2 = table_manager.add_row(final_table, 'سرمایه در گردش', 2)
    final_row3 = table_manager.add_row(final_table, 'جمع کل پروژه', 3)
    
    # تنظیم فرمول‌های ارجاع بین فصول
    final_fixed_col = final_table.columns.get(name='مبلغ')
    
    # ایجاد ستون‌های جداگانه برای هر ارجاع
    table_manager.add_column(final_table, 'مبلغ سرمایه گردش', 'reference', 3, 'ریال', 'SUM[مواد اولیه.هزینه سالانه]')
    table_manager.add_column(final_table, 'جمع نهایی', 'calculated', 4, 'ریال', '[سرمایه‌گذاری ثابت.مبلغ] + [this.مبلغ سرمایه گردش]')
    
    print("جدول 'خلاصه نهایی' ایجاد شد.")
    
    # محاسبه کل پروژه
    calc_engine = CalculationEngine(project)
    calc_engine.recalculate_project()
    
    print("\n=== محاسبات تکمیل شد ===")
    print(f"پروژه '{project.title}' با {project.chapters.count()} فصل ایجاد شد.")
    
    # نمایش نتایج
    print("\n=== نتایج محاسبات ===")
    
    # نمایش جدول زمین و ساختمان
    print("\n🏗️ زمین و ساختمان:")
    land_data = table_manager.get_table_data(land_table)
    for row in land_data['rows']:
        label = row['label']
        cells = row['cells']
        metraj = cells.get('متراژ', {}).get('value', 0)
        price = cells.get('قیمت واحد', {}).get('value', 0)
        total = cells.get('جمع کل', {}).get('value', 0)
        print(f"  {label}: {metraj} متر × {price:,} = {total:,} ریال")
    
    # نمایش جدول ماشین‌آلات
    print("\n⚙️ ماشین‌آلات:")
    machinery_data = table_manager.get_table_data(machinery_table)
    for row in machinery_data['rows']:
        label = row['label']
        cells = row['cells']
        count = cells.get('تعداد', {}).get('value', 0)
        price = cells.get('قیمت واحد', {}).get('value', 0)
        total = cells.get('جمع کل', {}).get('value', 0)
        print(f"  {label}: {count} عدد × {price:,} = {total:,} ریال")
    
    # نمایش جدول مواد اولیه
    print("\n📦 مواد اولیه:")
    materials_data = table_manager.get_table_data(materials_table)
    for row in materials_data['rows']:
        label = row['label']
        cells = row['cells']
        monthly_amount = cells.get('مقدار ماهانه', {}).get('value', 0)
        price = cells.get('قیمت واحد', {}).get('value', 0)
        monthly_cost = cells.get('هزینه ماهانه', {}).get('value', 0)
        yearly_cost = cells.get('هزینه سالانه', {}).get('value', 0)
        print(f"  {label}: {monthly_amount:,} کیلوگرم × {price:,} = {monthly_cost:,} ریال/ماه ({yearly_cost:,} ریال/سال)")
    
    print(f"\n✅ پروژه نمونه با موفقیت ایجاد شد!")
    print(f"🔗 ID پروژه: {project.id}")
    
    return project


if __name__ == '__main__':
    project = create_sample_project()
    print(f"\nپروژه آماده استفاده است. ID: {project.id}") 