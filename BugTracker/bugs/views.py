
from django.shortcuts import render, redirect, get_object_or_404
from .models import Bug, Project
from .forms import BugForm, ProjectForm, Project, SignUpForm
from django.http import JsonResponse, HttpResponse
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
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView


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

            # user = form.save()
            # login(request, user)
            # return redirect('login')  # Redirect to your project_list view
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

def ChangePassword(request):
    return render(request, 'bugs/change-password.html')

def ResetPassword(request):
    return render(request,'bugs/reset-password.html')

def project_list(request):
    projects = Project.objects.all()
    for project in projects:
        project.code = project.name[:3].upper()
    return render(request,  'bugs/project_list.html', {'projects': projects})


def delete_project(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(id=project_id)
        project.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'bugs/create_project.html', {'form': form})
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

    return render(request, 'bugs/bug_list.html', {'bugs': bugs, 'project_name': project.name,
                                                  'project_id': project_id,
                                                  'open_count': open_count,
                                                  'in_progress_count': in_progress_count,
                                                  'reopen_count': reopen_count,
                                                  'close_count': close_count,
                                                  'done_count': done_count,
                                                  })

@login_required
def create_bug(request, project_id):
    if request.method == 'POST':
        form = BugForm(request.POST, request.FILES)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.project_id = project_id     # Set the project_id for the bug
            bug.reporter = request.user.username  # Set the reporter to the username of the logged-in user
            bug.save()
            return redirect('bug_list', project_id=project_id)
    else:
        form = BugForm()
        project = Project.objects.get(id=project_id)
    return render(request, 'bugs/create_bug.html', {'form': form, 'project_name': project.name,
                                                    'project_id': project_id})
@login_required
def update_bug_status(request, bug_id):
    if request.method == 'POST':
        bug = Bug.objects.get(id=bug_id)
        new_status = request.POST.get('status')
        command = request.POST.get('command', '')
        bug.update = request.user.username  # Set the update bugs user to the username of the logged-in user
        current_history = bug.history or ''  # Get the current history or initialize as an empty string

        # Convert the current time to the desired timezone
        tz = pytz.timezone('Asia/Dubai')  # Replace with your desired timezone
        current_time = timezone.localtime(timezone.now(), tz)

        # timestamp = timezone.now()
        # current_time = timezone.localtime(timezone.now())
        formatted_time = current_time.strftime('%d-%m-%Y, %I:%M %p')

        # Add the new command to the history
        new_history = (f"{current_history}\n{bug.update}  {formatted_time}:\nStatus updated to {new_status}, "
                       f"Comment: {command}")

        bug.command = command
        bug.history = new_history

        # Update the bug status
        bug.status = new_status
        bug.save()

        success_message = f'Bug status updated to {new_status}'
        history_entry = (f'{bug.update}  {formatted_time}: \nStatus updated to {new_status}, Comment: {bug.command}')
        return JsonResponse({'status': 'success', 'message': success_message,
                             'history_entry': history_entry})

# def download_bug_report(request, project_id):
#     # project = Project.objects.get(id=project_id)  # Get the project
#
#     # Retrieve the project and bugs for the report
#     project = get_object_or_404(Project, pk=project_id)
#     bugs = Bug.objects.filter(project=project)
#
#     # Create a response object with appropriate content type for CSV
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = f'attachment; filename="{project.name}_bug_report.xlsx"'
#
#     # Create an Excel workbook and add a worksheet
#     workbook = xlsxwriter.Workbook(response, {'in_memory': True})
#     worksheet = workbook.add_worksheet()
#
#     # Define bold format
#     bold_format = workbook.add_format({'bold': True})
#
#     # Write the project name in bold as the first row
#     worksheet.write('A1', f'Project:  {project.name}', bold_format)
#
#     # Add two empty rows for separation
#     worksheet.write('A2', '')  # Empty row 1
#     worksheet.write('A3', '')  # Empty row 2
#
#     # Write the table headings with bold formatting
#     headings = ['Bug ID', 'Title', 'Description', 'Created At', 'Status']
#     for col_num, heading in enumerate(headings):
#         worksheet.write(4, col_num, heading, bold_format)
#
#     # Write the bug data rows
#     for row_num, bug in enumerate(bugs, start=5):
#             worksheet.write(row_num, 0, bug.bug_id)
#             worksheet.write(row_num, 1, bug.title)
#             worksheet.write(row_num, 2, bug.description)
#             worksheet.write(row_num, 3, bug.created_at.strftime('%Y-%m-%d %H:%M:%S'))  # Convert to string)
#             worksheet.write(row_num, 4, bug.status)
#
#     workbook.close()
#
#     return response

# def generate_pdf_report(request, project_id):
#     project = get_object_or_404(Project, pk=project_id)
#     bugs = Bug.objects.filter(project=project)
#
#     template = get_template('bugs/pdf_report_template.html')
#     context = {'project': project, 'bugs': bugs}
#     html = template.render(context)
#
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{project.name}_bug_report.pdf"'
#
#     pisa_status = pisa.CreatePDF(html, dest=response)
#
#     if pisa_status.err:
#         return HttpResponse('An error occurred while generating the PDF')
#
#     return response

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
        Paragraph(f'Status Count:', getSampleStyleSheet()[ 'Heading3']),
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
