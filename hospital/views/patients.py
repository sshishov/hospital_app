from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django import forms

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


class PatientForm(forms.ModelForm):

    class Meta:
        model = hospital_models.Patient
        fields = ('full_name', 'birthday',)
        widgets = {
            'birthday': forms.SelectDateWidget(
                attrs={
                    'class': 'form-control snps-inline-select'
                }
            ),
        }

    def clean(self):
        if hospital_models.Patient.objects.filter(
                full_name=self.cleaned_data['full_name'],
                birthday=self.cleaned_data['birthday']
        ).exists():
            raise forms.ValidationError(_("Patient already exists"))


class PatientList(ListView):
    model = hospital_models.Patient


class PatientCreate(CreateView):
    model = hospital_models.Patient
    form_class = PatientForm
    success_url = reverse_lazy('patient-create')


class PatientUpdate(UpdateView):
    model = hospital_models.Patient
    success_url = reverse_lazy('patient-list')
    fields = ('full_name', 'birthday',)


class PatientDelete(DeleteView):
    model = hospital_models.Patient
    success_url = reverse_lazy('patient-list')
