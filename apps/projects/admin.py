from django.contrib import admin
from .models import Project, ProjectVersion

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'business_type', 'created_at')
    list_filter = ('business_type', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
    date_hierarchy = 'created_at'

@admin.register(ProjectVersion)
class ProjectVersionAdmin(admin.ModelAdmin):
    list_display = ('project', 'version_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('project__title',)
