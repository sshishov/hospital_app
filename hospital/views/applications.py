from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .. import forms as hospital_forms, models as hospital_models


def manage_applications(request):
    if request.method == 'POST':
        formset = hospital_forms.ApplicationFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            formset = hospital_forms.ApplicationFormSet()
    else:
        formset = hospital_forms.ApplicationFormSet()
    return render(request, 'hospital/base_formset.html', {'formset': formset})


class ApplicationList(ListView):
    model = hospital_models.Application


class ApplicationCreate(CreateView):
    model = hospital_models.Application
    success_url = reverse_lazy('application-list')
    fields = ('name',)


class ApplicationUpdate(UpdateView):
    model = hospital_models.Application
    success_url = reverse_lazy('application-list')
    fields = ('name',)


class ApplicationDelete(DeleteView):
    model = hospital_models.Application
    success_url = reverse_lazy('application-list')
