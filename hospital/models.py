import logging
import uuid

from django.utils.translation import ugettext_lazy as _

from mongoengine import fields, document
from djongo import models

logger = logging.getLogger(__name__)


class AbstractTimestampModel(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name=_('ID'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Updated'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Added'))

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
    name = models.CharField(max_length=30, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Parameter')
        verbose_name_plural = _('Parameters')


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


class Form(AbstractTimestampModel):
    name = models.CharField(max_length=30, verbose_name=_('Name'))
    fields = models.ArrayReferenceField(to='hospital.Parameter', null=True, blank=True, verbose_name=_('Fields'))
    # fields = models.ManyToManyField(to='hospital.Parameter', verbose_name=_('Fields'))

    class Meta:
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')


class Application(AbstractTimestampModel):
    doctor = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name=_('Doctor'))
    patient = models.ForeignKey('hospital.Patient', on_delete=models.CASCADE, verbose_name=_('Patient'))
    project = models.ForeignKey('hospital.Project', on_delete=models.CASCADE, verbose_name=_('Project'))
    values = models.ArrayModelField(model_container=ParameterValue, verbose_name=_('Values'))

    class Meta:
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')
