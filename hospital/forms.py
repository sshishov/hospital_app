from django.forms import modelformset_factory

from . import models as hospital_models


ParameterFormSet = modelformset_factory(hospital_models.Parameter, fields=('name', 'description'), can_delete=True)
