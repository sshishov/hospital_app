from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from . import forms as hospital_forms, models as hospital_models


class HomeView(View):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def manage_parameters(request):
    if request.method == 'POST':
        formset = hospital_forms.ParameterFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            formset.save()
            formset = hospital_forms.ParameterFormSet()
    else:
        formset = hospital_forms.ParameterFormSet()
    return render(request, 'hospital/parameter_set.html', {'formset': formset})


class ParameterList(ListView):
    model = hospital_models.Parameter


class ParameterCreate(CreateView):
    model = hospital_models.Parameter
    success_url = reverse_lazy('parameter_list')
    fields = ('name', 'description')


class ParameterUpdate(UpdateView):
    model = hospital_models.Parameter
    success_url = reverse_lazy('parameter_list')
    fields = ('name', 'description')


class ParameterDelete(DeleteView):
    model = hospital_models.Parameter
    success_url = reverse_lazy('parameter_list')
