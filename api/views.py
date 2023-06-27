from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer, ProjectSerializer

from .models import User, Project


def get_user_instance_by_id(id):
    try:
        return User.objects.get(id=id)
    except User.DoesNotExist:
        return None


def my_middleware(request):
    if not request.data['user_id']:
        return Response('Bad Request')
    user = get_user_instance_by_id(request.data['user_id'])
    if not user:
        return Response('Bad Request')
    request.data['user'] = user
    request.data['owner'] = user.id


@api_view(['GET'])
def home(request):
    return Response('API Base Point')


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.register(serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    else:
        return Response('Bad Request')


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        request.data['confirm_password'] = request.data['password']
        request.data['pseudo'] = 'pseudo'
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.login(serializer.validated_data)
            return Response({'id': user.id, 'email': user.email, 'pseudo': user.pseudo})
        else:
            return Response(serializer.errors)
    else:
        return Response('Bad Request')


# Project

@api_view(['POST'])
def create_project(request):
    my_middleware(request)
    if request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.create_project(serializer.validated_data)
            return Response({'id': project.id, 'name': project.name, 'owner': project.owner.id})
        else:
            return Response(serializer.errors)
    else:
        return Response('Bad Request')


@api_view(['GET'])
def get_project(request, project_id):
    my_middleware(request)
    if request.method == 'GET':
        project = Project.objects.get(id=project_id, owner=request.data['owner'])
        return Response({'id': project.id, 'name': project.name, 'owner': project.owner.id})
    else:
        return Response('Bad Request')


@api_view(['PUT'])
def update_project(request, project_id):
    my_middleware(request)
    if request.method == 'PUT':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.update_project(project_id, serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    else:
        return Response('Bad Request')
