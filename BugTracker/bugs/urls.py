from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('auth/signup/', views.signup, name='signup'),
    path('auth/login/', views.CustomLoginView.as_view(), name='login'),

    path('bugs/change-password/', views.ChangePassword, name='changepassword'),
    path('bugs/reset-password/', views.ResetPassword, name='resetpassword'),

    path('projects/', views.project_list, name='project_list'),
    path('delete/<int:project_id>/', views.delete_project, name='delete_project'),
    path('projects/create/', views.create_project, name='create_project'),

    path('bugs/<int:project_id>/', views.bug_list, name='bug_list'),
    path('bugs/<int:project_id>/create/', views.create_bug, name='create_bug'),
    path('bugs/report/<int:project_id>/', views.generate_pdf_report, name='generate_pdf_report'),
    # path('bugs/download_bug_report/<int:project_id>/', views.download_bug_report, name='download_bug_report'),
    path('bugs/<int:bug_id>/update_status/', views.update_bug_status, name='update_bug_status'),
]
