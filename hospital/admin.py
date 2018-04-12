from django.contrib import admin

from . import models


class PatientAdmin(admin.ModelAdmin):
    pass


class ParameterAdmin(admin.ModelAdmin):
    pass


class ProjectAdmin(admin.ModelAdmin):
    pass


class Applicationdmin(admin.ModelAdmin):
    pass


class FormAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Parameter, ParameterAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Application, Applicationdmin)
admin.site.register(models.Form, FormAdmin)