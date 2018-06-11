from django import forms

from . import models as hospital_models
from .forms import fields as form_fields


class ParameterFactory(object):
    PARAMETER_TYPE_MAP = {
        hospital_models.Parameter.PARAMETER_TYPE_INTEGER: form_fields.HospitalIntegerField,
        hospital_models.Parameter.PARAMETER_TYPE_DECIMAL: form_fields.HospitalDecimalField,
        hospital_models.Parameter.PARAMETER_TYPE_STRING: form_fields.HospitalCharField,
        hospital_models.Parameter.PARAMETER_TYPE_MULTISTRING: form_fields.HospitalTextField,
        hospital_models.Parameter.PARAMETER_TYPE_BOOLEAN: form_fields.HospitalBooleanField,
        hospital_models.Parameter.PARAMETER_TYPE_DATE: form_fields.HospitalDateField,
        hospital_models.Parameter.PARAMETER_TYPE_DATETIME: form_fields.HospitalDateTimeField,
        hospital_models.Parameter.PARAMETER_TYPE_SELECT: form_fields.HospitalSelectField,
        hospital_models.Parameter.PARAMETER_TYPE_SELECT_MULTIPLE: form_fields.HospitalSelectMultipleField,
    }

    @classmethod
    def get(cls, field, *args, **kwargs):
        params = {**kwargs, **field.extra_params}
        return cls.PARAMETER_TYPE_MAP[field.field_type](*args, **params)


def make_form_fields(request, form):

    class FormFields(forms.Form):

        def __init__(self, *args, **kwargs):
            super(FormFields, self).__init__(*args, **kwargs)
            for field in form.fields.all():
                self.fields[str(field.id)] = ParameterFactory.get(field)
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
