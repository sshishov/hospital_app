from django import forms

from . import widgets


class HospitalIntegerField(forms.IntegerField):
    pass


class HospitalDecimalField(forms.DecimalField):
    pass


class HospitalCharField(forms.CharField):
    pass


class HospitalTextField(forms.CharField):
    widget = forms.Textarea


class HospitalBooleanField(forms.BooleanField):
    widget = widgets.HospitalCheckboxInput


class HospitalDateField(forms.DateField):
    input_formats = ('%d.%m.%Y',)
    widget = widgets.HospitalDateInput


class HospitalDateTimeField(forms.DateTimeField):
    input_formats = ('%d.%m.%Y H:i:s',)
    widget = widgets.HospitalDateTimeInput


class HospitalSelectField(forms.ChoiceField):

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = [('', '---')] + kwargs.get('choices', [])
        super(HospitalSelectField, self).__init__(*args, **kwargs)


class HospitalSelectMultipleField(forms.MultipleChoiceField):

    def __init__(self, *args, **kwargs):
        super(HospitalSelectMultipleField, self).__init__(*args, **kwargs)
