import logging
import uuid

from django.utils.translation import ugettext_lazy as _

from mongoengine import fields, document
from djongo import models
from django import forms

logger = logging.getLogger(__name__)


class AbstractTimestampModel(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name=_('ID'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Added'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    @property
    def id(self):
        return self._id

    class Meta:
        abstract = True


class Patient(AbstractTimestampModel):
    name = models.CharField(max_length=50, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')


class Parameter(AbstractTimestampModel):

    PARAMETER_TYPE_INTEGER = 1
    PARAMETER_TYPE_STRING = 2
    PARAMETER_TYPES = (
        (PARAMETER_TYPE_INTEGER, _('Integer')),
        (PARAMETER_TYPE_STRING, _('String')),
    )
    PARAMETER_TYPE_MAP = {
        PARAMETER_TYPE_INTEGER: forms.IntegerField(),
        PARAMETER_TYPE_STRING: forms.CharField(),
    }

    name = models.CharField(max_length=30, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    type = models.IntegerField(choices=PARAMETER_TYPES, verbose_name=_('Type'))

    class Meta:
        verbose_name = _('Parameter')
        verbose_name_plural = _('Parameters')

    def get_type(self):
        return self.PARAMETER_TYPE_MAP[self.type]

    def __str__(self):
        return self.name


class ParameterValue(AbstractTimestampModel):
    parameter = models.EmbeddedModelField(model_container=Parameter, verbose_name=_('Parameter'))
    value = models.CharField(max_length=100, verbose_name=_('Value'))

    class Meta:
        abstract = True


class Project(AbstractTimestampModel):
    name = models.CharField(max_length=30, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.name


class Form(AbstractTimestampModel):
    name = models.CharField(max_length=30, verbose_name=_('Name'))
    # fields = models.ArrayReferenceField(to='hospital.Parameter', null=True, blank=True, verbose_name=_('Fields'))
    fields = models.ManyToManyField(to='hospital.Parameter', verbose_name=_('Fields'))

    class Meta:
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')

    def form_fields(self):
        fields = [field.name for field in self.fields.all()]
        return ', '.join(fields)


class Application(AbstractTimestampModel):
    doctor = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name=_('Doctor'))
    patient = models.ForeignKey('hospital.Patient', on_delete=models.CASCADE, verbose_name=_('Patient'))
    project = models.ForeignKey('hospital.Project', on_delete=models.CASCADE, verbose_name=_('Project'))
    values = models.ArrayModelField(model_container=ParameterValue, verbose_name=_('Values'))

    class Meta:
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')


# user extension models
class UserProfile(AbstractTimestampModel):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, verbose_name=_('Full Name'))
    city = models.CharField(max_length=100, verbose_name=_('City'))
    subject = models.CharField(max_length=100, verbose_name=_('Subject'))
    district = models.CharField(max_length=100, verbose_name=_('District'))
    projects = models.ManyToManyField(to='hospital.Project', verbose_name=_('Projects'))

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return self.full_name
