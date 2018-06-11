from django import forms
from django.utils.translation import pgettext_lazy

from .. import models as hospital_models
from .. import widgets


class SelectForm(forms.Form):
    patient = forms.ModelChoiceField(
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
    form = forms.ModelChoiceField(
        queryset=hospital_models.Form.objects.none(),
        widget=forms.Select(
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