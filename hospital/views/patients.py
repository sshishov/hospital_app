from datetime import date

from django.urls import reverse_lazy
from django.utils.translation import pgettext_lazy
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

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        field = self.fields.get('full_name')
        if field:
            field.widget.attrs.update(
                {'placeholder': field.label}
            )
            field.label = ''


    class Meta:
        model = hospital_models.Patient
        fields = ('full_name', 'birthday',)
        widgets = {
            'birthday': forms.SelectDateWidget(
                years=range(1920, date.today().year + 1),
                attrs={
                    'class': 'form-control'
                }
            ),
        }

    def clean(self):
        if hospital_models.Patient.objects.filter(
                full_name=self.cleaned_data['full_name'],
                birthday=self.cleaned_data['birthday']
        ).exists():
            raise forms.ValidationError(pgettext_lazy('error_msg', 'Patient already exists'))


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
