from django.contrib import admin

# Register your models here.

from .models import User, Project, Task, Status


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'password', 'pseudo')


admin.site.register(User)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Status)
