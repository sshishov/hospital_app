from django.forms import modelformset_factory

from . import models as hospital_models


ParameterFormSet = modelformset_factory(hospital_models.Parameter, fields=('name', 'description'), can_delete=True)
PatientFormSet = modelformset_factory(hospital_models.Patient, fields=('full_name', 'birthday',), can_delete=True)
ProjectFormSet = modelformset_factory(hospital_models.Project, fields=('name',), can_delete=True)
FormFormSet = modelformset_factory(hospital_models.Form, fields=('name',), can_delete=True)
ApplicationFormSet = modelformset_factory(hospital_models.Application, fields=('project', 'doctor', 'patient'), can_delete=True)
