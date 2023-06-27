from django.urls import path
from .views import home, register, login, create_project, update_project

urlpatterns = [
    path('', home),
    path('register', register),
    path('login', login),
    path('project', create_project),
    path('project/<int:project_id>', update_project),
]