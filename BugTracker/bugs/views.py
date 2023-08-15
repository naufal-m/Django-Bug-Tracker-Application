from django.shortcuts import render, redirect
from .models import Bug, Project
from .forms import BugForm, ProjectForm
from django.http import JsonResponse



# Create your views here.
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'bugs/project_list.html', {'projects': projects})

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
    return render(request, 'bugs/bug_list.html', {'bugs': bugs, 'project_name': project.name, 'project_id': project_id})

def create_bug(request, project_id):
    if request.method == 'POST':
        form = BugForm(request.POST)
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
        bug.status = new_status
        bug.save()

        success_message = f'Bug status updated to {new_status}'
        return JsonResponse({'status': 'success', 'message': success_message})
