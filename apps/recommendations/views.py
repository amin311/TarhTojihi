# apps/recommendations/views.py

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Recommendation
from apps.projects.models import Project

def recommendations_home(request):
    """صفحه‌ی اصلی مدیریت توصیه‌ها."""
    return HttpResponse("مدیریت پیشنهاد طرح‌های مشابه")

def recommendation_list(request, project_id):
    """فهرست پیشنهادها برای یک پروژه."""
    project = get_object_or_404(Project, pk=project_id)
    recs = Recommendation.objects.filter(project=project)
    return render(request, 'recommendations/recommendation_list.html', {'project': project, 'recs': recs})
