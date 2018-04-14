from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .. import forms as hospital_forms, models as hospital_models


def manage_forms(request):
    if request.method == 'POST':
        formset = hospital_forms.FormFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            formset = hospital_forms.FormFormSet()
    else:
        formset = hospital_forms.FormFormSet()
    return render(request, 'hospital/base_formset.html', {'formset': formset})


class FormList(ListView):
    model = hospital_models.Form


class FormCreate(CreateView):
    model = hospital_models.Form
    success_url = reverse_lazy('form-list')
    fields = ('name', 'fields')

    def post(self, request, *args, **kwargs):
        fields = request.POST.pop('fields', [])
        instance = super().post(request, *args, **kwargs)
        return instance.fields.add(fields)


class FormUpdate(UpdateView):
    model = hospital_models.Form
    success_url = reverse_lazy('form-list')
    fields = ('name', 'fields')


class FormDelete(DeleteView):
    model = hospital_models.Form
    success_url = reverse_lazy('form-list')
