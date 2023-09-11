from django.urls import path
from . import views

urlpatterns = [
    path('auth/signup/', views.signup, name='signup'),
    path('auth/login/', views.CustomLoginView.as_view(), name='login'),
    path('auth/home/', views.home_page, name='home'),

    path('bugs/auth/forgot_password/', views.forgot_password, name='forgot_password'),
    path('bugs/reset-password-form/<str:token>/', views.reset_password, name='reset_password'),

    path('projects/', views.project_list, name='project_list'),
    path('delete/<int:project_id>/', views.delete_project, name='delete_project'),
    path('projects/create/', views.create_project, name='create_project'),

    path('create/bugs/<int:project_id>/', views.bug_list, name='bug_list'),
    path('bugs/<int:project_id>/create/', views.create_bug, name='create_bug'),
    path('bugs/<int:project_id>/update-status/<int:bug_id>/', views.update_bug_status, name='update_bug_status'),

    path('bugs/report/<int:project_id>/', views.generate_pdf_report, name='generate_pdf_report'),
]
