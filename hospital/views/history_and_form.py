from django.shortcuts import render
from django import forms
from django.utils.translation import ugettext_lazy as _

from hospital import models as hospital_models


class PatientSelect(forms.Select):

    objects = None

    def get_context(self, *args, **kwargs):
        self.objects = {obj.id: obj for obj in self.choices.queryset}
        return super(PatientSelect, self).get_context(*args, **kwargs)

    def create_option(self, *args, **kwargs):
        option = super(PatientSelect, self).create_option(*args, **kwargs)
        option['attrs']['data-subtext'] = self.objects[args[1]].birthday.strftime('%d.%m.%Y')
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
        queryset=hospital_models.Form.objects.none(),
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

    def __init__(self, data, *args, **kwargs):
        super(SelectForm, self).__init__(data, *args, **kwargs)
        project = data.get('project')
        if project:
            self.fields['form'].queryset = hospital_models.Form.objects.filter(project=project)



def make_form_fields(request, form):

    class FormFields(forms.Form):

        def __init__(self, *args, **kwargs):
            super(FormFields, self).__init__(*args, **kwargs)
            for field in form.fields.all():
                self.fields[str(field.id)] = field.type()
                self.fields[str(field.id)].label = field.name
                self.fields[str(field.id)].widget.attrs.update({
                    'placeholder': field.name,
                    'data-content': field.description,
                    'data-toggle': 'popover',
                    'class': 'col-8',
                })

        def save(self):
            hospital_models.Application.objects.create(
                doctor=request.user,
                patient_id=request.session['patient'],
                form=form,
                values=[
                    hospital_models.ParameterValue(
                        parameter=hospital_models.Parameter.objects.get(pk=pk),
                        value=value,
                    ) for pk, value in self.cleaned_data.items()
                ],
            )
    # fields = {'patient': forms.UUIDField(widget=forms.HiddenInput())}
    # for field in form.fields.all():
    #     fields[field.name] = field.get_type()
    # return type('FormFields', (forms.BaseForm,), {'base_fields': fields})
    return FormFields


def manage_view(request):
    form_to_fill = None
    history_list = []
    patient_form = SelectForm(request.session)
    if patient_form.is_valid():
        patient = patient_form.cleaned_data['patient']
        form = patient_form.cleaned_data['form']
        if form:
            form_to_fill = make_form_fields(request, form)()
        history_list = hospital_models.Application.objects.filter(
            patient=patient, form__project=request.session.get('project'),
        )
    if request.method == 'POST':
        form = make_form_fields(request, form)(data=request.POST)
        if form.is_valid():
            form.save()
    return render(
        request=request,
        template_name='hospital/history_and_form.html',
        context={
            'patient_form': patient_form,
            'history_list': history_list,
            'form_to_fill': form_to_fill,
        },
    )
