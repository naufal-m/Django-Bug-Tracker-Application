from django.shortcuts import render, redirect, get_object_or_404
from .models import Bug, Project
from .forms import BugForm, ProjectForm
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
import pytz



# Create your views here.
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

    # return render(request, 'bugs/bug_list.html', {
        # ... your existing context ...
        'open_count': open_count,
        'in_progress_count': in_progress_count,
        'reopen_count': reopen_count,
        'close_count': close_count,
        'done_count': done_count,
    })


def create_bug(request, project_id):
    if request.method == 'POST':
        form = BugForm(request.POST, request.FILES)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.project_id = project_id # Set the project_id for the bug
            bug.save()
            return redirect('bug_list', project_id=project_id)
    else:
        form = BugForm()
        project = Project.objects.get(id=project_id)
    return render(request, 'bugs/create_bug.html', {'form': form, 'project_name': project.name, 'project_id': project_id})

def update_bug_status(request, bug_id):
    if request.method == 'POST':
        bug = Bug.objects.get(id=bug_id)
        new_status = request.POST.get('status')
        command = request.POST.get('command', '')
        current_history = bug.history or ''  # Get the current history or initialize as an empty string

        # Convert the current time to the desired timezone
        tz = pytz.timezone('Asia/Dubai')  # Replace with your desired timezone
        current_time = timezone.localtime(timezone.now(), tz)

        # timestamp = timezone.now()
        # current_time = timezone.localtime(timezone.now())
        formatted_time = current_time.strftime('%d-%m-%Y, %I:%M %p')

        new_history = f"{current_history}\n{formatted_time}: Status updated to {new_status}, Comment: {command}"  # Add the new command to the history
        bug.history = new_history

# Update the bug status
        bug.status = new_status
        bug.save()

        success_message = f'Bug status updated to {new_status}'
        history_entry = f'{formatted_time}: Status updated to {new_status}, Comment: {command}'
        return JsonResponse({'status': 'success', 'message': success_message, 'history_entry': history_entry})
