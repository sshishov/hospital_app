from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .. import forms as hospital_forms, models as hospital_models


def manage_patients(request):
    if request.method == 'POST':
        formset = hospital_forms.PatientFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            formset = hospital_forms.PatientFormSet()
    else:
        formset = hospital_forms.PatientFormSet()
    return render(request, 'hospital/base_formset.html', {'formset': formset})


class PatientList(ListView):
    model = hospital_models.Patient


class PatientCreate(CreateView):
    model = hospital_models.Patient
    success_url = reverse_lazy('patient-list')
    fields = ('name',)


class PatientUpdate(UpdateView):
    model = hospital_models.Patient
    success_url = reverse_lazy('patient-list')
    fields = ('name',)


class PatientDelete(DeleteView):
    model = hospital_models.Patient
    success_url = reverse_lazy('patient-list')
