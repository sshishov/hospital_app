from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .. import forms as hospital_forms, models as hospital_models


def manage_projects(request):
    if request.method == 'POST':
        formset = hospital_forms.ProjectFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            formset = hospital_forms.ProjectFormSet()
    else:
        formset = hospital_forms.ProjectFormSet()
    return render(request, 'hospital/base_formset.html', {'formset': formset})


class ProjectList(ListView):
    model = hospital_models.Project


class ProjectCreate(CreateView):
    model = hospital_models.Project
    success_url = reverse_lazy('project-list')
    fields = ('name',)


class ProjectUpdate(UpdateView):
    model = hospital_models.Project
    success_url = reverse_lazy('project-list')
    fields = ('name',)


class ProjectDelete(DeleteView):
    model = hospital_models.Project
    success_url = reverse_lazy('project-list')
