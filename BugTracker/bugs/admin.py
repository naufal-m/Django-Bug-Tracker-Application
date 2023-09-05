from django.contrib import admin
from .models import Bug, Project, Profile, Image, BugHistory

# Register your models here.
admin.site.register(Project)     # Register the project model
admin.site.register(Bug)
admin.site.register(Profile)
admin.site.register(Image)
admin.site.register(BugHistory)
