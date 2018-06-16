from django.contrib import admin as django_admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models as hospital_models


class PatientAdmin(django_admin.ModelAdmin):
    pass


class ParameterAdmin(django_admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    ordering = ('name',)


class ProjectAdmin(django_admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


class ApplicationAdmin(django_admin.ModelAdmin):
    pass


class FormAdmin(django_admin.ModelAdmin):
    list_display = ('name', 'form_fields', 'created_at', 'updated_at')


class UserProfileInline(django_admin.StackedInline):
    model = hospital_models.UserProfile
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Register other required models for admin part
django_admin.site.register(hospital_models.User, UserAdmin)
django_admin.site.register(hospital_models.Patient, PatientAdmin)
django_admin.site.register(hospital_models.Parameter, ParameterAdmin)
django_admin.site.register(hospital_models.Project, ProjectAdmin)
django_admin.site.register(hospital_models.Application, ApplicationAdmin)
django_admin.site.register(hospital_models.Form, FormAdmin)
