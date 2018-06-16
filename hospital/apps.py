from django.apps import AppConfig

from django.utils.translation import pgettext_lazy


class HospitalConfig(AppConfig):
    name = 'hospital'
    verbose_name = pgettext_lazy('app_name', 'Hospital')
