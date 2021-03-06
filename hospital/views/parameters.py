from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .. import forms as hospital_forms, models as hospital_models


def manage_parameters(request):
    if request.method == 'POST':
        formset = hospital_forms.ParameterFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            formset = hospital_forms.ParameterFormSet()
    else:
        formset = hospital_forms.ParameterFormSet()
    return render(request, 'hospital/base_formset.html', {'formset': formset})


class ParameterList(ListView):
    model = hospital_models.Parameter


class ParameterCreate(CreateView):
    model = hospital_models.Parameter
    success_url = reverse_lazy('parameter-list')
    fields = ('name', 'description')


class ParameterUpdate(UpdateView):
    model = hospital_models.Parameter
    success_url = reverse_lazy('parameter-list')
    fields = ('name', 'description')


class ParameterDelete(DeleteView):
    model = hospital_models.Parameter
    success_url = reverse_lazy('parameter-list')

