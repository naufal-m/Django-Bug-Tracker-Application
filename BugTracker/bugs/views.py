from django.shortcuts import render, redirect, get_object_or_404
import json
from django.urls import reverse
from django.db.models import Q, Max
from django.template import Template, Context
from django.utils.html import linebreaks

from .models import Bug, Project, Profile, Image, BugHistory
from .forms import BugForm, ProjectForm, Project, SignUpForm, ForgotPassword, PasswordResetForm, UpdateBugForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from datetime import datetime
from django.utils import timezone
import pytz, csv, xlsxwriter
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

from reportlab.lib.pagesizes import letter, landscape, portrait, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, LongTable, PageBreak, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.db.models import F
import textwrap

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, password_validation
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView

from .emails import (send_forget_password_mail, send_bug_assigned_email, send_registration_invitation_email,
                     send_project_invitation_email)
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import uuid


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            #   new line added
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            form.save()

            new_user = authenticate(username=username, password=password)
            if new_user is not None:
                login(request, new_user)
                return redirect('login')
        else:
            print(form.errors)
            # Display error messages if form is not valid
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {form.fields[field_name].label}: {error}")
    else:
        form = SignUpForm()
    return render(request, 'bugs/signup.html', {'form': form})


class CustomLoginView(LoginView, TemplateView):
    template_name = 'bugs/login.html'  # Replace with the actual template path

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect('project_list')  # Redirect to the 'project_list' page

    def form_invalid(self, form):
        messages.error(self.request, "Login failed, Username or password is incorrect.")
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        response = super(LoginView, self).get(request, *args, **kwargs)
        messages = self.request.session.get('messages', [])  # Get messages from session
        self.request.session['messages'] = []  # Clear messages from session
        response.context_data['messages'] = messages  # Add messages to the template context
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return response


def change_password(request):
    if request.method == 'POST':
        form = ForgotPassword(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:

                user = User.objects.get(email=email)
                user_id = user.id
                print(user_id)

                token = str(uuid.uuid4())

                #   check if a profile already exist for the user
                try:
                    profile = Profile.objects.get(user_id=user_id)
                except Profile.DoesNotExist:
                    print("Hello")
                    # Save the token and related information to the Profile model
                    # profile = Profile(user=user)
                    profile = Profile.objects.create(user=user, forget_password_token=token, created_at=datetime.now())
                    profile.save()

                profile.forget_password_token = token
                profile.created_at = datetime.now()
                profile.save()

                send_forget_password_mail(email, token)

                messages.success(request, 'An email has been sent.')

            except User.DoesNotExist:
                print("User not found")

    else:
        form = ForgotPassword()
    return render(request, 'bugs/change-password.html', {'form': form})


def ResetPassword(request, token):
    valid_token = True
    profile_obj = Profile.objects.get(forget_password_token=token)
    print(profile_obj)

    context = {
        'valid_token': valid_token,
        'form': PasswordResetForm
    }
    return render(request, 'bugs/reset-password.html', context)


@login_required
def project_list(request):
    user = request.user
    # projects = Project.objects.all()

    projects = Project.objects.filter(Q(created_user=user) | Q(users=user)).distinct()

    # for project in user_projects:
    #     project.code = project.name[:3].upper()

    return render(request, 'bugs/project_list.html', {'projects': projects})


@login_required
def delete_project(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(id=project_id)
        project.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():

            # Parse the entered emails and associate users with the project
            email_list = [email.strip() for email in form.cleaned_data['users'].split(',')]
            users = User.objects.filter(email__in=email_list)
            project = form.save(commit=False)
            project.created_user = request.user
            project.save()
            project.users.set(users)  # Associate users with the project

            # Get the list of email addresses added in the 'users' field
            user_emails = form.cleaned_data['users'].split(',')

            for email in user_emails:
                email = email.strip()  # Remove extra spaces

                # Check if the email corresponds to a registered user or non register user
                try:
                    user = User.objects.get(email=email)
                    # Send email to registered users
                    send_project_invitation_email(project, user)

                except User.DoesNotExist:
                    # Send email to unregistered users
                    send_registration_invitation_email(project, email)

            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'bugs/create_project.html', {'form': form})


@login_required
def bug_list(request, project_id):
    # bugs = Bug.objects.all()
    # bugs = Bug.objects.filter(project_id=project_id, reporter=request.user.username)
    # reporter=request.user.username --> indicates the bug list of created user after logged in.
    bugs = Bug.objects.filter(project_id=project_id)
    project = Project.objects.get(id=project_id)

    # Calculate bug counts by status
    open_count = Bug.objects.filter(project=project_id, status='Open').count()
    in_progress_count = Bug.objects.filter(project=project_id, status='In Progress').count()
    reopen_count = Bug.objects.filter(project=project_id, status='Re-open').count()
    close_count = Bug.objects.filter(project=project_id, status='Close').count()
    done_count = Bug.objects.filter(project=project_id, status='Done').count()

    #   assigned user filter
    assigned_filter = request.GET.get('assigned_filter')
    if assigned_filter and assigned_filter != 'all':
        bugs = bugs.filter(assigned_to=assigned_filter)

    creator_user = project.created_user
    associated_user = project.users.all()

    combined_users = associated_user | User.objects.filter(pk=creator_user.pk)
    bug_history_entries = BugHistory.objects.all()

    last_updated_times = {}
    last_closed_updated_times = {}

    for bug in bugs:
        last_updated_time = BugHistory.objects.filter(
            bug=bug,
        ).aggregate(Max('updated_at'))['updated_at__max']

        last_closed_updated_time = BugHistory.objects.filter(
            bug=bug,
            status='Close'
        ).aggregate(Max('updated_at'))['updated_at__max']

        last_updated_times[bug.id] = last_updated_time
        last_closed_updated_times[bug.id] = last_closed_updated_time

    context = {
        'bugs': bugs,
        'project_name': project.name,
        'project_id': project_id,
        'users': combined_users,
        'open_count': open_count,
        'in_progress_count': in_progress_count,
        'reopen_count': reopen_count,
        'close_count': close_count,
        'done_count': done_count,
        'bug_history_entries': bug_history_entries,
        'last_updated_times': last_updated_times,
        'last_closed_updated_times': last_closed_updated_times,
    }

    return render(request, 'bugs/bug_list.html', context)

@login_required
def create_bug(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        # form = BugForm(request.POST, request.FILES, user=request.user)
        form = BugForm(project, request.POST, request.FILES)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.project_id = project_id  # Set the project_id for the bug
            bug.reporter = request.user.username  # Set the reporter to the username of the logged-in user
            bug.assigned = form.cleaned_data['assigned_to']
            bug.save()

            # Use the send_bug_assigned_email function to send the email
            send_bug_assigned_email(bug)

            return redirect('bug_list', project_id=project_id)
    else:
        # form = BugForm(user=request.user)
        form = BugForm(project=project)

        project = Project.objects.get(id=project_id)
    return render(request, 'bugs/create_bug.html', {'form': form, 'project_name': project.name,
                                                    'project_id': project_id})


@login_required
def update_bug_status(request, project_id, bug_id):
    if request.method == 'POST':
        form = UpdateBugForm(request.POST)
        if form.is_valid():
            bug = Bug.objects.get(id=bug_id)
            project = get_object_or_404(Project, id=bug.project_id)
            new_status = request.POST.get('status')
            command = request.POST.get('command2', '')
            uploaded_image = request.FILES.get('images')
            bug.update = request.user.username  # Set the update bugs user to the username of the logged-in user

            bug.save()

            # Create a new BugHistory entry
            history_entry = BugHistory(
                bug=bug,
                project=project,
                comments=command,
                status=new_status,
                status_assigned_user=bug.update,
                report_user=request.user,
                bug_id_code=bug.bug_id,
            )
            history_entry.save()

            # Handle image upload
            if uploaded_image:
                # Create a SimpleUploadedFile from the uploaded image
                uploaded_image_file = SimpleUploadedFile(uploaded_image.name, uploaded_image.read())
                history_entry.images.save(uploaded_image.name, uploaded_image_file)

            bug.status = new_status
            bug.comment = command
            bug.save()

            context = {
                'form': form,
                'project_id': project_id,
            }

            return render(request, 'bugs/bug_list.html', context)

    else:
        form = UpdateBugForm()
    return render(request, 'bugs/bug_list.html', {'form': form})

@login_required
def generate_pdf_report(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    bugs = Bug.objects.filter(project=project)

    # Calculate bug counts by status
    open_count = bugs.filter(status='Open').count()
    in_progress_count = bugs.filter(status='In Progress').count()
    reopen_count = bugs.filter(status='Re-open').count()
    close_count = bugs.filter(status='Close').count()
    done_count = bugs.filter(status='Done').count()

    # Create a buffer to store the PDF content
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=portrait(A4))

    # Create a list to hold the data for the paragraphs
    paragraphs = [
        Paragraph(f'Project Name: {project.name}', getSampleStyleSheet()['Heading1']),
        Paragraph(f'Status Count:', getSampleStyleSheet()['Heading3']),
        Paragraph(f'Open:           {open_count}', getSampleStyleSheet()['Normal']),
        Paragraph(f'In Progress:    {in_progress_count}', getSampleStyleSheet()['Normal']),
        Paragraph(f'Re-open:        {reopen_count}', getSampleStyleSheet()['Normal']),
        Paragraph(f'Close:          {close_count}', getSampleStyleSheet()['Normal']),
        Paragraph(f'Done:           {done_count}', getSampleStyleSheet()['Normal']),
        PageBreak()  # Add a page break before the table
    ]

    # Create a ReportLab PDF document
    doc = SimpleDocTemplate(buffer, pagesize=portrait(letter))
    story = []

    # Create a list to hold the data for the table
    data = [
        ['Bug Report:'],
        [
            'Bug ID',
            'Title',
            'Description',
            'Status',
            'Created At',
            'Created By',
        ]
    ]

    # Add data from the queryset to the table
    for bug in bugs:
        # images = [str(image.image) for image in bug.bug_images.all()]

        # Wrap the title and description text
        title_wrapped = "\n".join(textwrap.wrap(bug.title, width=25))
        description_wrapped = "\n".join(textwrap.wrap(bug.description, width=40))

        data.append([
            bug.bug_id,
            title_wrapped,
            description_wrapped,
            bug.status,
            bug.created_at.strftime('%d-%m-%Y %I:%M %p'),
            bug.reporter
        ])

    # col_widths = [50, 200,None, None,None]

    # Create the table and style
    table = Table(data)

    # table = LongTable(data, colWidths=col_widths)
    style = TableStyle([
        ('BACKGROUND', (0, 1), (-1, 1), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12)
    ])
    # ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    # ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Add line separators
    for i in range(1, len(data)):
        style.add('LINEBELOW', (0, i), (-1, i), 1, colors.black)

    table.setStyle(style)

    # Build the PDF document
    doc.build(paragraphs + [table])
    buffer.seek(0)

    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{project.name}_bug_report.pdf"'

    return response
