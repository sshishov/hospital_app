from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

from .. import factory, forms, models as hospital_models


@permission_required('hospital.manage_application', raise_exception=True)
def manage_view(request):
    form_to_fill = None
    history_list = []

    # generate form and history list
    patient_form = forms.SelectForm(request.session)
    if patient_form.is_valid():
        # generate selected form
        patient = patient_form.cleaned_data['patient']
        form = patient_form.cleaned_data['form']
        if form:
            form_to_fill = factory.make_form_fields(request, form)()

        # generate history list for selected patient
        history_list = hospital_models.Application.objects.filter(
            patient=patient, form__project=request.session.get('project'),
        )

        if not request.user.has_perm('hospital.supervise_application'):
            history_list = history_list.filter(doctor=request.user.id)

    # check and save application
    if request.method == 'POST':
        form = factory.make_form_fields(request, form)(data=request.POST)
        if form.is_valid():
            form.save()

    # render view
    return render(
        request=request,
        template_name='hospital/history_and_form.html',
        context={
            'patient_form': patient_form,
            'history_list': history_list,
            'form_to_fill': form_to_fill,
        },
    )
