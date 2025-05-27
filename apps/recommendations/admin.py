from django.contrib import admin
from .models import Recommendation

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('project', 'score')
    search_fields = ('project__title',)
    list_filter = ('score',)
