from django import forms
from .models import Bug, Project

class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['title', 'description']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']