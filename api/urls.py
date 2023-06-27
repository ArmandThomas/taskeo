from django.urls import path
from .views import home, register, login, get_projects, create_project, update_project, create_statuses, get_statuses, update_status

urlpatterns = [
    path('', home),
    path('register', register),
    path('login', login),

    path('get_projects', get_projects),
    path('create_project', create_project),
    path('project/<int:project_id>', update_project),

    path('get_statuses', get_statuses),
    path('create_status', create_statuses),
    path('status/<int:status_id>', update_status),

]