import logging
import uuid

from mongoengine import fields, document
from djongo import models

logger = logging.getLogger(__name__)


class AbstractTimestampModel(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # _id = models.ObjectIdField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def id(self):
        return self._id

    class Meta:
        abstract = True


class Client(AbstractTimestampModel):
    name = models.CharField(max_length=50)


class Parameter(AbstractTimestampModel):
    name = models.CharField(max_length=30)
    description = models.TextField()


class ParameterValue(AbstractTimestampModel):
    parameter = models.EmbeddedModelField(model_container=Parameter)
    value = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Project(AbstractTimestampModel):
    name = models.CharField(max_length=30)


class Form(AbstractTimestampModel):
    name = models.CharField(max_length=30)
    fields = models.ArrayReferenceField(to='hospital.Parameter', null=True, blank=True)


class Application(AbstractTimestampModel):
    doctor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    client = models.ForeignKey('hospital.Client', on_delete=models.CASCADE)
    project = models.ForeignKey('hospital.Project', on_delete=models.CASCADE)
    values = models.ArrayModelField(model_container=ParameterValue)
