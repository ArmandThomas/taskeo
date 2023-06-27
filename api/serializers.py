from rest_framework import serializers
from api.models import User, Project, Status

import bcrypt


class UserSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def register(self, validated_data):


        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError("Email already exists")

        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")

        if len(validated_data['password']) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in validated_data['password']):
            raise serializers.ValidationError('Password must contain at least 1 digit')
        if not any(char.isupper() for char in validated_data['password']):
            raise serializers.ValidationError('Password must contain at least 1 uppercase character')
        if not any(char.islower() for char in validated_data['password']):
            raise serializers.ValidationError('Password must contain at least 1 lowercase character')
        if not any(char in ['$', '@', '#', '%', '&', '*', '!', '?'] for char in validated_data['password']):
            raise serializers.ValidationError('Password must contain at least 1 special character')

        validated_data.pop('confirm_password')
        validated_data['password'] = bcrypt.hashpw(validated_data['password'].encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')

        user = User(
            email=validated_data['email'],
            password=validated_data['password'],
            pseudo=validated_data['pseudo']
        )
        user.save()
        return user

    def login(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError('Email and password are required')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise serializers.ValidationError('Incorrect password')

        return user

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def create_project(self, validated_data):
        project = Project(
            name=validated_data['name'],
            owner=validated_data['owner']
        )
        project.save()
        return project

    def update_project(self, project_id, validated_data):
        project = Project.objects.get(id = project_id)
        if project.owner != validated_data['owner']:
            raise serializers.ValidationError('You are not the owner of this project')
        project.name = validated_data['name']
        project.save()
        return project

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

    def create_status(self, validated_data):
        status = Status(
            name=validated_data['name'],
            project=validated_data['project'],
        )
        status.save()
        return status

    def update_status(self, status_id, validated_data):
        status = Status.objects.get(id = status_id)
        if status.owner != validated_data['owner']:
            raise serializers.ValidationError('You are not the owner of this status')
        status.name = validated_data['name']
        status.save()
        return status

