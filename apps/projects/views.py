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
