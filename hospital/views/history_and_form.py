from django.shortcuts import render
from django import forms
from django.utils.translation import ugettext_lazy as _

from hospital import models as hospital_models


class PatientSelect(forms.Select):
    def __init__(self, attrs=None):
        super(PatientSelect, self).__init__(attrs)
        self.patients = {patient._id: patient.birthday for patient in
                         hospital_models.Patient.objects.all()}

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(PatientSelect, self).create_option(name, value, label, selected, index, subindex=None, attrs=None)
        date_string = self.patients[value].strftime('%d.%m.%Y')
        option['attrs']['data-subtext'] = date_string
        return option


class SelectForm(forms.Form):
    patient = forms.ModelChoiceField(
        queryset=hospital_models.Patient.objects.all(),
        widget=PatientSelect(
            attrs={
                'class': 'selectpicker',
                'onchange': 'this.form.submit()',
                'data-live-search': 'true',
                'data-show-subtext': 'true',
                'title': _('Choose Patient'),
                'data-width': '500px',
            }
        ),
        empty_label=None,
    )
    form = forms.ModelChoiceField(
        queryset=hospital_models.Form.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'selectpicker',
                'onchange': 'this.form.submit()',
                'data-live-search': 'true',
                'title': _('Choose Form'),
            }
        ),
        empty_label=None,
        required=False
    )

    class Meta:
        widgets = {
            'patients': forms.Select(attrs={'class': 'selectpicker'})
        }


def make_form_fields(form, patient):
    fields = {'patient': forms.UUIDField(widget=forms.HiddenInput())}
    for field in form.fields.all():
        fields[field.name] = field.get_type()
    return type('FormFields', (forms.BaseForm,), {'base_fields': fields})


def manage_view(request):
    form_to_fill = None
    history_list = []
    patient_form = SelectForm(request.session)
    if patient_form.is_valid():
        patient = patient_form.cleaned_data['patient']
        form = patient_form.cleaned_data['form']
        if form:
            form_to_fill = make_form_fields(form, patient)(initial={'patient': patient.id})
        history_list = hospital_models.Application.objects.filter(
            patient=patient, project=request.session.get('project'),
        )
    return render(
        request=request,
        template_name='hospital/history_and_form.html',
        context={
            'patient_form': patient_form,
            'history_list': history_list,
            'form_to_fill': form_to_fill,
        },
    )
