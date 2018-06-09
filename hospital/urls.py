from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, reverse_lazy
from django.views import defaults as default_views, generic as generic_views

from . import views as hospital_views


urlpatterns = [
    # auth
    path(route='accounts/', view=include('django.contrib.auth.urls')),
    path(route='accounts/profile/', view=hospital_views.profile.get_profile, name='profile'),

    # common
    path(route='{url}/'.format(url=settings.ADMIN_URL), view=admin.site.urls),
    path(route='', view=generic_views.RedirectView.as_view(pattern_name='history_and_form'), name='index'),
    path(route='i18n/', view=include('django.conf.urls.i18n')),
    path(route='history_and_form/', view=hospital_views.history_and_form.manage_view, name='history_and_form'),

    # session settings
    path(route='accounts/session/', view=hospital_views.session_settings.update_session_data, name='update_data'),

    # NOT USED VIEWS AND URLS
    # path(route='', view=hospital_views.home.HomeView.as_view(), name='index'),
    #
    # # parameters views
    # path(route='parameters_set/', view=hospital_views.parameters.manage_parameters, name='parameter-set'),
    # path(route='parameters/', view=hospital_views.parameters.ParameterList.as_view(), name='parameter-list'),
    # path(route='parameters/create/', view=hospital_views.parameters.ParameterCreate.as_view(), name='parameter-create'),
    # path(route='parameters/<uuid:pk>/update/', view=hospital_views.parameters.ParameterUpdate.as_view(), name='parameter-update'),
    # path(route='parameters/<uuid:pk>/delete/', view=hospital_views.parameters.ParameterDelete.as_view(), name='parameter-delete'),
    #
    # # patients views
    # path(route='patients_set/', view=hospital_views.patients.manage_patients, name='patient-set'),
    # path(route='patients/', view=hospital_views.patients.PatientList.as_view(), name='patient-list'),
    path(route='patients/create/', view=hospital_views.patients.PatientCreate.as_view(), name='patient-create'),
    # path(route='patients/<uuid:pk>/update/', view=hospital_views.patients.PatientUpdate.as_view(), name='patient-update'),
    # path(route='patients/<uuid:pk>/delete/', view=hospital_views.patients.PatientDelete.as_view(), name='patient-delete'),
    #
    # # projects views
    # path(route='projects_set/', view=hospital_views.projects.manage_projects, name='project-set'),
    # path(route='projects/', view=hospital_views.projects.ProjectList.as_view(), name='project-list'),
    # path(route='projects/create/', view=hospital_views.projects.ProjectCreate.as_view(), name='project-create'),
    # path(route='projects/<uuid:pk>/update/', view=hospital_views.projects.ProjectUpdate.as_view(),
    #      name='project-update'),
    # path(route='projects/<uuid:pk>/delete/', view=hospital_views.projects.ProjectDelete.as_view(),
    #      name='project-delete'),
    #
    # # forms views
    # path(route='forms_set/', view=hospital_views.forms.manage_forms, name='form-set'),
    # path(route='forms/', view=hospital_views.forms.FormList.as_view(), name='form-list'),
    # path(route='forms/create/', view=hospital_views.forms.FormCreate.as_view(), name='form-create'),
    # path(route='forms/<uuid:pk>/update/', view=hospital_views.forms.FormUpdate.as_view(),
    #      name='form-update'),
    # path(route='forms/<uuid:pk>/delete/', view=hospital_views.forms.FormDelete.as_view(),
    #      name='form-delete'),
    #
    # # applications views
    # path(route='applications_set/', view=hospital_views.applications.manage_applications, name='application-set'),
    # path(route='applications/', view=hospital_views.applications.ApplicationList.as_view(), name='application-list'),
    # path(route='applications/create/', view=hospital_views.applications.ApplicationCreate.as_view(), name='application-create'),
    # path(route='applications/<uuid:pk>/update/', view=hospital_views.applications.ApplicationUpdate.as_view(),
    #      name='application-update'),
    # path(route='applications/<uuid:pk>/delete/', view=hospital_views.applications.ApplicationDelete.as_view(),
    #      name='application-delete'),
]

handler403 = 'hospital.views.errors.permission_denied'

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar  # pylint:disable=import-error

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
