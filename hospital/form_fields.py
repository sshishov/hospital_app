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
    input_formats = ('%d.%m.%Y',)
    widget = HospitalDateInput


class HospitalDateTimeField(forms.DateTimeField):
    input_formats = ('%d.%m.%Y H:i:s',)
    widget = HospitalDateTimeInput


class HospitalSelectField(forms.ChoiceField):

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = [('', '---'), ('a', 'a'), ('b', 'b'), ('c', 'c')]
        super(HospitalSelectField, self).__init__(*args, **kwargs)


class HospitalSelectMultipleField(forms.MultipleChoiceField):

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = [('a', 'a'), ('b', 'b'), ('c', 'c')]
        super(HospitalSelectMultipleField, self).__init__(*args, **kwargs)
