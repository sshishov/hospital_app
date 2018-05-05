from urllib.parse import unquote

from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.utils.http import is_safe_url

from hospital import models as hospital_models


class ProjectSessionForm(forms.Form):
    project = forms.ModelChoiceField(
        queryset=hospital_models.Project.objects.all(),
    )

    def save(self, request):
        request.session['project'] = str(self.cleaned_data['project'].id)
        if 'patient' in request.session:
            del request.session['patient']
        if 'form' in request.session:
            del request.session['form']


class PatientSessionForm(forms.Form):
    patient = forms.ModelChoiceField(
        queryset=hospital_models.Patient.objects.all(),
    )

    def save(self, request):
        request.session['patient'] = str(self.cleaned_data['patient'].id)


class FormSessionForm(forms.Form):
    form = forms.ModelChoiceField(
        queryset=hospital_models.Form.objects.all(),
    )

    def save(self, request):
        request.session['form'] = str(self.cleaned_data['form'].id)


def update_session_data(request):
    next = request.POST.get('next', request.GET.get('next'))
    if ((next or not request.is_ajax()) and
            not is_safe_url(url=next, allowed_hosts={request.get_host()}, require_https=request.is_secure())):
        next = request.META.get('HTTP_REFERER')
        if next:
            next = unquote(next)  # HTTP_REFERER may be encoded.
        if not is_safe_url(url=next, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            next = '/'
    response = HttpResponseRedirect(next) if next else HttpResponse(status=204)
    if request.method == 'POST':
        form = ProjectSessionForm(request.POST)
        if form.is_valid():
            form.save(request)
        form = PatientSessionForm(request.POST)
        if form.is_valid():
            form.save(request)
        form = FormSessionForm(request.POST)
        if form.is_valid():
            form.save(request)
    return response
