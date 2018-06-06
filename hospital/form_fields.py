from django import forms


class HospitalDateInput(forms.DateInput):
    # input_type = 'date'  TODO: Delete if not needed

    def __init__(self, attrs=None, format=None):
        if attrs is None:
            attrs = {}
        attrs['data-provide'] = 'datepicker'
        super().__init__(attrs, format)


class HospitalDateTimeInput(forms.DateTimeInput):
    # input_type = 'datetime-local'  TODO: Delete if not needed

    def __init__(self, attrs=None, format=None):
        if attrs is None:
            attrs = {}
        attrs['data-provide'] = 'datetimepicker'
        super().__init__(attrs, format)


class HospitalCheckboxInput(forms.CheckboxInput):
    template_name = 'widgets/checkbox.html'


class HospitalTextField(forms.CharField):
    widget = forms.Textarea


class HospitalBooleanField(forms.BooleanField):
    widget = HospitalCheckboxInput


class HospitalDateField(forms.DateField):
    widget = HospitalDateInput


class HospitalDateTimeField(forms.DateTimeField):
    widget = HospitalDateTimeInput
