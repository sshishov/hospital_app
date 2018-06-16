from django import forms

from jsoneditor.fields.django_jsonfield import JSONFormField

from .. import models as hospital_models


class ParameterForm(forms.ModelForm):

    extra_params = JSONFormField(required=False, initial={})

    class Meta:
        model = hospital_models.Parameter
        fields = ('name', 'description', 'field_type', 'extra_params')
