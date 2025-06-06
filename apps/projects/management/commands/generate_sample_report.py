import os
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from weasyprint import HTML
from apps.projects.models import Project
from apps.finance.models import ProjectFinancialData
from django.conf import settings

class Command(BaseCommand):
    help = 'یک گزارش PDF نمونه برای یک پروژه مشخص تولید می‌کند'

    def handle(self, *args, **options):
        project_id = 1
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'پروژه با شناسه {project_id} یافت نشد.'))
            return

        financial_data = ProjectFinancialData.objects.filter(project=project).select_related('financial_table')

        context = {
            'project': project,
            'financial_data': financial_data
        }

        html_string = render_to_string('pdf/report_template.html', context)
        html = HTML(string=html_string)

        # ساخت پوشه در صورت عدم وجود
        output_folder = os.path.join(settings.MEDIA_ROOT, 'reports')
        os.makedirs(output_folder, exist_ok=True)
        
        output_path = os.path.join(output_folder, f'TarhTojihi_Project_{project.id}.pdf')

        try:
            html.write_pdf(output_path)
            self.stdout.write(self.style.SUCCESS(f'گزارش PDF با موفقیت در مسیر زیر ذخیره شد:'))
            self.stdout.write(output_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR('خطا در تولید PDF. آیا پیش‌نیازهای WeasyPrint (مانند GTK3) نصب شده است؟'))
            self.stdout.write(str(e)) 