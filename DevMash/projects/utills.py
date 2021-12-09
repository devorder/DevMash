from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def search_projects(request):
    search_query = ''
    tags = ''
    if request.GET.get('project_search'):
        search_query = request.GET.get('project_search')
        tags = Tag.objects.filter(name__icontains=search_query)
    projectsList = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
        )
    return projectsList,search_query


def paginate_projects(request, projectsList, results):
    page = request.GET.get('page')
    paginator = Paginator(projectsList, results)
    try:
        projectsList = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projectsList = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projectsList = paginator.page(page)

    left_index = int(page)-1
    if left_index < 1:
        left_index = 1
    right_index = int(page)+2
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1 
    custom_range = range(left_index, right_index)
    return custom_range,projectsList,paginator