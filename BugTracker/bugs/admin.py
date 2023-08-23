from django.contrib import admin
from .models import Bug, Project

# Register your models here.
admin.site.register(Project)     # Register the project model
admin.site.register(Bug)
