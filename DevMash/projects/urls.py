from django.urls import path

from . import views

urlpatterns = [
    path('', views.projects, name="project_list"),
    path('project/<str:project_id>/', views.project, name="project"),
    path('create-project/', views.create_project, name="create-project"),
    path('update-project/<str:project_id>/', views.update_project, name="update-project"),
    path('delete-project/<str:project_id>/', views.delete_project, name="delete-project")
]
