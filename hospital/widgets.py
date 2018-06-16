from django import forms


class HospitalDateInput(forms.DateInput):
    # input_type = 'date'  TODO: Delete if not needed

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['data-provide'] = 'datepicker'
        return context


class HospitalDateTimeInput(forms.DateTimeInput):
    # input_type = 'datetime-local'  TODO: Delete if not needed

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['data-provide'] = 'datetimepicker'
        return context


class HospitalCheckboxInput(forms.CheckboxInput):
    template_name = 'widgets/checkbox.html'


class HospitalSelect(forms.Select):

    @staticmethod
    def _choice_has_empty_value(choice):
        return True


class HospitalMultiSelect(forms.SelectMultiple):
    pass


class PatientSelect(forms.Select):

    objects = None

    def get_context(self, *args, **kwargs):
        self.objects = {obj.id: obj for obj in self.choices.queryset}
        return super(PatientSelect, self).get_context(*args, **kwargs)

    def create_option(self, *args, **kwargs):
        option = super(PatientSelect, self).create_option(*args, **kwargs)
        option['attrs']['data-subtext'] = self.objects[args[1]].birthday.strftime('%d.%m.%Y')
        return option
