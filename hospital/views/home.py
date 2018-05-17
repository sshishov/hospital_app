from django.shortcuts import render
from django.views import View

from .. import models as hospital_models


class HomeView(View):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        projects = hospital_models.Project.objects.all()
        return render(request, self.template_name, {'projects': projects})
