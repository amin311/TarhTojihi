# apps/projects/forms.py
from django import forms
from .models import Project

class ProjectStep1Form(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProjectStep2Form(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['business_type']
        widgets = {
            'business_type': forms.Select(attrs={'class': 'form-select'}),
        }
