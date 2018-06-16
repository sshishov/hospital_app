import ast
from collections import defaultdict
import datetime
import logging
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import pgettext, pgettext_lazy

from djongo import models
from djongo.models import json

from . import utils

logger = logging.getLogger(__name__)

CODE_MAX_LENGTH = 10


class AbstractTimestampModel(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name=pgettext_lazy('model_field', 'ID'), editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=pgettext_lazy('model_field', 'Added'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=pgettext_lazy('model_field', 'Updated'))

    @property
    def id(self):
        return self._id

    class Meta:
        abstract = True


class User(AbstractTimestampModel, AbstractUser):

    class Meta:
        verbose_name = pgettext_lazy('model_name', 'User')
        verbose_name_plural = pgettext_lazy('model_name', 'Users')


class Patient(AbstractTimestampModel):
    full_name = models.CharField(max_length=100, verbose_name=pgettext_lazy('model_field', 'Full Name'))
    birthday = models.DateField(verbose_name=pgettext_lazy('model_field', 'Birthday'))

    class Meta:
        verbose_name = pgettext_lazy('model_name', 'Patient')
        verbose_name_plural = pgettext_lazy('model_name', 'Patients')

    def __str__(self):
        return self.full_name


class Parameter(AbstractTimestampModel):

    PARAMETER_TYPE_INTEGER = 1
    PARAMETER_TYPE_DECIMAL = 2
    PARAMETER_TYPE_STRING = 3
    PARAMETER_TYPE_MULTISTRING = 4
    PARAMETER_TYPE_BOOLEAN = 5
    PARAMETER_TYPE_DATE = 6
    PARAMETER_TYPE_DATETIME = 7
    PARAMETER_TYPE_SELECT = 8
    PARAMETER_TYPE_SELECT_MULTIPLE = 9
    PARAMETER_TYPES = (
        (PARAMETER_TYPE_INTEGER, pgettext_lazy('field_type', 'Integer')),
        (PARAMETER_TYPE_STRING, pgettext_lazy('field_type', 'String')),
        (PARAMETER_TYPE_DECIMAL, pgettext_lazy('field_type', 'Decimal')),
        (PARAMETER_TYPE_MULTISTRING, pgettext_lazy('field_type', 'Multistring')),
        (PARAMETER_TYPE_BOOLEAN, pgettext_lazy('field_type', 'Boolean')),
        (PARAMETER_TYPE_DATE, pgettext_lazy('field_type', 'Date')),
        (PARAMETER_TYPE_DATETIME, pgettext_lazy('field_type', 'Datetime')),
        (PARAMETER_TYPE_SELECT, pgettext_lazy('field_type', 'Select')),
        (PARAMETER_TYPE_SELECT_MULTIPLE, pgettext_lazy('field_type', 'Select Multiple')),
    )

    REQUIRED = (
        PARAMETER_TYPE_INTEGER,
        PARAMETER_TYPE_DECIMAL,
        PARAMETER_TYPE_STRING,
        PARAMETER_TYPE_MULTISTRING,
        PARAMETER_TYPE_BOOLEAN,
        PARAMETER_TYPE_DATE,
        PARAMETER_TYPE_DATETIME,
        PARAMETER_TYPE_SELECT,
        PARAMETER_TYPE_SELECT_MULTIPLE,
    )
    CHOICES = (
        PARAMETER_TYPE_SELECT,
        PARAMETER_TYPE_SELECT_MULTIPLE,
    )

    name = models.CharField(max_length=30, verbose_name=pgettext_lazy('model_field', 'Name'))
    description = models.TextField(verbose_name=pgettext_lazy('model_field', 'Description'))
    field_type = models.IntegerField(choices=PARAMETER_TYPES, verbose_name=pgettext_lazy('model_field', 'Type'))
    extra_params = json.JSONField(default=dict, verbose_name=pgettext_lazy('model_field', 'Extra Parameters'))

    class Meta:
        verbose_name = pgettext_lazy('model_name', 'Parameter')
        verbose_name_plural = pgettext_lazy('model_name', 'Parameters')

    def __str__(self):
        return self.name

    def clean(self):
        cleaned_data = super().clean()
        available = []
        errors = defaultdict(list)
        if self.field_type in self.REQUIRED:
            required = self.extra_params.get('required', False)
            available.append('required')
            if not isinstance(required, bool):
                errors['extra_params'].append(pgettext('error_msg', 'Field `required` should be boolean'))
            self.extra_params['required'] = required
        if self.field_type in self.CHOICES:
            available.extend(['choices', 'search_support'])
            search = self.extra_params.get('search_support', False)
            choices = self.extra_params.get('choices', [])
            if not isinstance(search, bool):
                errors['extra_params'].append(pgettext('error_msg', 'Field `search_support` should be boolean'))
            if not isinstance(choices, (list, tuple)):
                errors['extra_params'].append(pgettext('error_msg', 'Field `choices` should be iterable'))
            else:
                for item in choices:
                    if not isinstance(item, str):
                        errors['extra_params'].append(
                            pgettext(
                                'error_msg', '{item}: Field `choices` should consist of strings',
                            ).format(item=item),
                        )
            self.extra_params['search_support'] = search
            self.extra_params['choices'] = choices

        if set(self.extra_params) - set(available):
            errors['extra_params'].append(
                pgettext(
                    'error_msg', 'Incorrect value provided: {incorrect_values}. Valid choices are: {available}',
                ).format(available=available, incorrect_values=set(self.extra_params) - set(available)),
            )
        if errors:
            raise ValidationError(errors)
        return cleaned_data


class ParameterValue(AbstractTimestampModel):
    parameter = models.EmbeddedModelField(model_container=Parameter, verbose_name=pgettext_lazy('model_field', 'Parameter'))
    value = models.CharField(max_length=100, verbose_name=pgettext_lazy('model_field', 'Value'))

    class Meta:
        abstract = True

    @property
    def get_wrapped_value(self):
        value = self.value
        if value is not None:
            if self.parameter.field_type == Parameter.PARAMETER_TYPE_MULTISTRING:
                value = '<pre>{value}</pre>'.format(value=value)
            elif self.parameter.field_type == Parameter.PARAMETER_TYPE_DATETIME:
                value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%i:%s').strftime('%m.%d.%Y %H:%i:%s')
            elif self.parameter.field_type == Parameter.PARAMETER_TYPE_DATE:
                value = datetime.datetime.strptime(value, '%Y-%m-%d').strftime('%m.%d.%Y')
            elif self.parameter.field_type == Parameter.PARAMETER_TYPE_SELECT:
                value = dict(utils.generate_choices(self.parameter.extra_params['choices'])).get(value)
            elif self.parameter.field_type == Parameter.PARAMETER_TYPE_SELECT_MULTIPLE:
                value = ', '.join(
                    [
                        dict(utils.generate_choices(self.parameter.extra_params['choices'])).get(value)
                        for value in ast.literal_eval(value)
                    ]
                )
        return value

    def __str__(self):
        return '{obj.parameter.name}={obj.value}'.format(obj=self)


class Project(AbstractTimestampModel):
    name = models.CharField(max_length=30, verbose_name=pgettext_lazy('model_field', 'Name'))
    code = models.CharField(max_length=CODE_MAX_LENGTH, verbose_name=pgettext_lazy('model_field', 'Code'))

    class Meta:
        verbose_name = pgettext_lazy('model_name', 'Project')
        verbose_name_plural = pgettext_lazy('model_name', 'Projects')

    def __str__(self):
        return self.name


class Form(AbstractTimestampModel):
    name = models.CharField(max_length=30, verbose_name=pgettext_lazy('model_field', 'Name'))
    # fields = models.ArrayReferenceField(to='hospital.Parameter', null=True, blank=True, verbose_name=pgettext_lazy('model_field', 'Fields'))
    fields = models.ManyToManyField(to='hospital.Parameter', related_name='parameter', verbose_name=pgettext_lazy('model_field', 'Fields'))
    project = models.ForeignKey(to='hospital.Project', on_delete=models.CASCADE, verbose_name=pgettext_lazy('model_field', 'Project'))
    code = models.CharField(max_length=CODE_MAX_LENGTH, verbose_name=pgettext_lazy('model_field', 'Code'))

    class Meta:
        verbose_name = pgettext_lazy('model_name', 'Form')
        verbose_name_plural = pgettext_lazy('model_name', 'Forms')

    def form_fields(self):
        fields = [field.name for field in self.fields.all()]
        return ', '.join(fields)

    def __str__(self):
        return self.name


class Application(AbstractTimestampModel):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=pgettext_lazy('model_field', 'Doctor'))
    patient = models.ForeignKey('hospital.Patient', on_delete=models.CASCADE, verbose_name=pgettext_lazy('model_field', 'Patient'))
    form = models.ForeignKey('hospital.Form', on_delete=models.CASCADE, verbose_name=pgettext_lazy('model_field', 'Form'))
    values = models.ArrayModelField(model_container=ParameterValue, verbose_name=pgettext_lazy('model_field', 'Values'))
    is_active = models.BooleanField(default=True, verbose_name=pgettext_lazy('model_field', 'Active'))
    parent = models.ForeignKey('hospital.Application', on_delete=models.CASCADE, verbose_name=pgettext_lazy('model_field', 'Parent'))

    class Meta:
        verbose_name = pgettext_lazy('model_name', 'Application')
        verbose_name_plural = pgettext_lazy('model_name', 'Applications')
        permissions = (
            ('manage_application', 'Can manage applications'),
            ('supervise_application', 'Can supervise applications per project'),
        )

    def __str__(self):
        return '{obj.form.project.code}:{obj.form.code}:{obj.values}'.format(obj=self)


# user extension models
class UserProfile(AbstractTimestampModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=pgettext_lazy('model_field', 'User'))
    city = models.CharField(max_length=100, verbose_name=pgettext_lazy('model_field', 'City'))
    subject = models.CharField(max_length=100, verbose_name=pgettext_lazy('model_field', 'Subject'))
    district = models.CharField(max_length=100, verbose_name=pgettext_lazy('model_field', 'District'))
    projects = models.ManyToManyField(to='hospital.Project', verbose_name=pgettext_lazy('model_field', 'Projects'))

    class Meta:
        verbose_name = pgettext_lazy('model_name', 'Profile')
        verbose_name_plural = pgettext_lazy('model_name', 'Profiles')

    def __str__(self):
        return self.user.get_full_name()
