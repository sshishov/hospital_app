from django import forms as django_forms
from django.utils.translation import pgettext_lazy

from .. import models as hospital_models
from .. import widgets


class SelectForm(django_forms.Form):
    patient = django_forms.ModelChoiceField(
        queryset=hospital_models.Patient.objects.all(),
        widget=widgets.PatientSelect(
            attrs={
                'class': 'selectpicker',
                'onchange': 'this.form.submit()',
                'data-live-search': 'true',
                'data-show-subtext': 'true',
                'title': pgettext_lazy('action', 'Choose Patient'),
                'data-width': '500px',
            }
        ),
        empty_label=None,
    )
    form = django_forms.ModelChoiceField(
        queryset=hospital_models.Form.objects.none(),
        widget=django_forms.Select(
            attrs={
                'class': 'selectpicker',
                'onchange': 'this.form.submit()',
                'data-live-search': 'true',
                'title': pgettext_lazy('action', 'Choose Form'),
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