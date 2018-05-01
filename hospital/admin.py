from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from . import models


class PatientAdmin(admin.ModelAdmin):
    pass


class ParameterAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at','updated_at']
    ordering = ['name']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']


class ApplicationAdmin(admin.ModelAdmin):
    pass


class FormAdmin(admin.ModelAdmin):
    list_display = ['name', 'form_fields', 'created_at', 'updated_at']


class UserProfileInline(admin.StackedInline):
    model = models.UserProfile
    can_delete = False
    verbose_name = 'Profile'
    verbose_name_plural = 'Profiles'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register other required models for admin part
admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Parameter, ParameterAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Application, ApplicationAdmin)
admin.site.register(models.Form, FormAdmin)
