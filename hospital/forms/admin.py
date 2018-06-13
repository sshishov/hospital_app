from django import forms
from django.utils.translation import pgettext_lazy

from jsoneditor.fields.django_jsonfield import JSONFormField

from .. import models as hospital_models


class ParameterForm(forms.ModelForm):
    REQUIRED = (
        hospital_models.Parameter.PARAMETER_TYPE_INTEGER,
        hospital_models.Parameter.PARAMETER_TYPE_DECIMAL,
        hospital_models.Parameter.PARAMETER_TYPE_STRING,
        hospital_models.Parameter.PARAMETER_TYPE_MULTISTRING,
        hospital_models.Parameter.PARAMETER_TYPE_BOOLEAN,
        hospital_models.Parameter.PARAMETER_TYPE_DATE,
        hospital_models.Parameter.PARAMETER_TYPE_DATETIME,
        hospital_models.Parameter.PARAMETER_TYPE_SELECT,
        hospital_models.Parameter.PARAMETER_TYPE_SELECT_MULTIPLE,
    )
    CHOICES = (
        hospital_models.Parameter.PARAMETER_TYPE_SELECT,
        hospital_models.Parameter.PARAMETER_TYPE_SELECT_MULTIPLE,
    )

    extra_params = JSONFormField(required=False, initial={})

    class Meta:
        model = hospital_models.Parameter
        fields = ('name', 'description', 'field_type', 'extra_params')

    def clean(self):
        cleaned_data = super(ParameterForm, self).clean()
        extra_params = cleaned_data.get('extra_params')
        field_type = cleaned_data.get('field_type')
        available = []
        if field_type in ParameterForm.REQUIRED:
            required = extra_params.get('required', False)
            available.append('required')
            if not isinstance(required, bool):
                self.add_error(
                    field='extra_params', error=pgettext_lazy('error_msg', 'Field `required` should be boolean'),
                )
            extra_params['required'] = required
        if field_type in ParameterForm.CHOICES:
            choices = extra_params.get('choices', [])
            available.append('choices')
            if not isinstance(choices, (list, tuple)):
                self.add_error(
                    field='extra_params', error=pgettext_lazy('error_msg', 'Field `choices` should be iterable'),
                )
            else:
                for item in choices:
                    if not isinstance(item, (list, tuple)) or len(item) != 2:
                        self.add_error(
                            field='extra_params',
                            error=pgettext_lazy(
                                'error_msg',
                                '{item}: Field `choices` should consist of iterables (value, description)'.format(
                                    item=item,
                                ),
                            ),
                        )
            extra_params['choices'] = choices

        if set(extra_params) - set(available):
            self.add_error(
                field='extra_params',
                error=pgettext_lazy(
                    'error_msg',
                    'Incorrect value provided: {incorrect_values}. Valid choices are: {available}'.format(
                        available=available, incorrect_values=set(extra_params) - set(available)
                    ),
                ),
            )
        else:
            cleaned_data['extra_params'] = extra_params
        return cleaned_data
