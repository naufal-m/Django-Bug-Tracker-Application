from django.urls import path
from . import views

urlpatterns = [
path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),
    path('bugs/<int:project_id>/', views.bug_list, name='bug_list'),
    path('bugs/<int:project_id>/create/', views.create_bug, name='create_bug'),
path('bugs/<int:bug_id>/update_status/', views.update_bug_status, name='update_bug_status'),
]
