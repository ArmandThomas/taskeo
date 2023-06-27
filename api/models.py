from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=500)
    pseudo = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class Project(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    priority = models.IntegerField(default=0)
    deadline = models.DateTimeField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " - " + self.project.name

class Status(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name