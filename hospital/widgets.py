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


class PatientSelect(forms.Select):

    objects = None

    def get_context(self, *args, **kwargs):
        self.objects = {obj.id: obj for obj in self.choices.queryset}
        return super(PatientSelect, self).get_context(*args, **kwargs)

    def create_option(self, *args, **kwargs):
        option = super(PatientSelect, self).create_option(*args, **kwargs)
        option['attrs']['data-subtext'] = self.objects[args[1]].birthday.strftime('%d.%m.%Y')
        return option
