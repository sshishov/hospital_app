import logging
import uuid

from django.utils.translation import ugettext_lazy as _

from mongoengine import fields, document
from djongo import models

logger = logging.getLogger(__name__)


class AbstractTimestampModel(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def id(self):
        return self._id

    class Meta:
        abstract = True


class Patient(AbstractTimestampModel):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')


class Parameter(AbstractTimestampModel):
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name = _('Parameter')
        verbose_name_plural = _('Parameters')


class ParameterValue(AbstractTimestampModel):
    parameter = models.EmbeddedModelField(model_container=Parameter)
    value = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Project(AbstractTimestampModel):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


class Form(AbstractTimestampModel):
    name = models.CharField(max_length=30)
    fields = models.ArrayReferenceField(to='hospital.Parameter', null=True, blank=True)

    class Meta:
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')


class Application(AbstractTimestampModel):
    doctor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    patient = models.ForeignKey('hospital.Patient', on_delete=models.CASCADE)
    project = models.ForeignKey('hospital.Project', on_delete=models.CASCADE)
    values = models.ArrayModelField(model_container=ParameterValue)

    class Meta:
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')
