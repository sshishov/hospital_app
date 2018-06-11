from django import forms

from . import widgets


class BaseHospitalFieldMixin(object):
    def __init__(self, *args, **kwargs):
        if 'required' not in kwargs:
            kwargs['required'] = False
        super(BaseHospitalFieldMixin, self).__init__(*args, **kwargs)


class HospitalTextField(BaseHospitalFieldMixin, forms.CharField):
    widget = forms.Textarea


class HospitalBooleanField(BaseHospitalFieldMixin, forms.BooleanField):
    widget = widgets.HospitalCheckboxInput


class HospitalDateField(BaseHospitalFieldMixin, forms.DateField):
    input_formats = ('%d.%m.%Y',)
    widget = widgets.HospitalDateInput


class HospitalDateTimeField(BaseHospitalFieldMixin, forms.DateTimeField):
    input_formats = ('%d.%m.%Y H:i:s',)
    widget = widgets.HospitalDateTimeInput


class HospitalSelectField(BaseHospitalFieldMixin, forms.ChoiceField):

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = [('', '---')] + kwargs.get('choices', [])
        super(HospitalSelectField, self).__init__(*args, **kwargs)


class HospitalSelectMultipleField(BaseHospitalFieldMixin, forms.MultipleChoiceField):

    def __init__(self, *args, **kwargs):
        super(HospitalSelectMultipleField, self).__init__(*args, **kwargs)
