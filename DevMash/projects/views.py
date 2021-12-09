from django.core import paginator
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from .forms import ProjectForm, ReviewForm
from .utills import search_projects, paginate_projects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError




def projects(request):
    projectsList,search_query = search_projects(request)
    custom_range,projectsList,paginator = paginate_projects(request, projectsList, 3)
    return render(request, "projects/projects.html", context={'projects': projectsList, 'search_query':search_query, 'paginator': paginator, 'custom_range': custom_range})
    
def project(request, project_id):
    project = Project.objects.get(id=project_id) 
    form = ReviewForm
    if request.method == 'POST':
        try:
            form = ReviewForm(request.POST)
            frm = form.save(commit=False)
            frm.project = project
            frm.owner = request.user.profile
            frm.save()
            project.getVoteCount
            messages.success(request, "Review added successfully.")
            return redirect('project', project_id=project.id)
        except IntegrityError:
            messages.error(request, "You already reviewed this project.")
            return redirect('project', project_id=project.id)
            
    # tags = project.tags.all()
    return render(request, 'projects/project.html', {'project': project, 'form': form})


@login_required(login_url='login')
def create_project(request):
    form = ProjectForm()
    profile = request.user.profile
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            frm = form.save(commit=False)
            frm.owner = profile
            frm.save()
            return redirect('user-account')
    ctx = {
        'form': form
        }
    return render(request, 'projects/project_form.html', context=ctx)

@login_required(login_url='login')
def update_project(request, project_id):
    profile = request.user.profile
    project = profile.project_set.get(id=project_id)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('user-account')
    ctx = {
        'form': form
        }
    return render(request, 'projects/project_form.html', context=ctx)
    
@login_required(login_url='login')
def delete_project(request, project_id):
    profile = request.user.profile
    project = profile.project_set.get(id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('user-account')
    return render(request, 'delete_template.html', context={'data' : project})