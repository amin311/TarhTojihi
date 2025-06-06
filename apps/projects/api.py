from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from .models import Project, ProjectVersion
from .serializers import ProjectSerializer, ProjectVersionSerializer
from apps.finance.models import ProjectFinancialData
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related('business_type', 'owner').all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # به‌صورت خودکار owner = request.user
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], url_path='generate-report')
    def generate_report(self, request, pk=None):
        """گزارش PDF طرح توجیهی را تولید می‌کند."""
        if not request.user.is_authenticated:
            return Response({'detail': 'ورود برای دریافت گزارش الزامی است.'}, status=403)

        project = self.get_object()
        financial_data = ProjectFinancialData.objects.filter(project=project).select_related('financial_table')

        context = {
            'project': project,
            'financial_data': financial_data
        }

        # تبدیل Jinja2 template به رشته HTML
        html_string = render_to_string('pdf/report_template.html', context)

        try:
            # رندر کردن HTML به PDF با WeasyPrint
            html = HTML(string=html_string)
            pdf_file = html.write_pdf()

            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="report_{project.id}.pdf"'
            return response

        except Exception as e:
            # این خطا معمولاً به دلیل عدم نصب GTK3 در ویندوز است
            return Response(
                {"error": "خطا در تولید PDF. لطفاً از نصب بودن پیش‌نیازهای WeasyPrint (مانند GTK3) اطمینان حاصل کنید.", "details": str(e)},
                status=500
            )


class ProjectVersionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectVersion.objects.select_related('project').all()
    serializer_class = ProjectVersionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return self.queryset.filter(project_id=project_id)
        return self.queryset 