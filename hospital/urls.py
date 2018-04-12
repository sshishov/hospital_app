from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views import defaults as default_views

from . import views as hospital_views


urlpatterns = [
    path(route=settings.ADMIN_URL, view=admin.site.urls),
    path(route='', view=hospital_views.HomeView.as_view()),
    path(route='i18n/', view=include('django.conf.urls.i18n')),

    path(route='parameters_set/', view=hospital_views.manage_parameters, name='parameter-set'),
    path(route='parameters/', view=hospital_views.ParameterList.as_view(), name='parameter-list'),
    path(route='parameters/create/', view=hospital_views.ParameterCreate.as_view(), name='parameter-create'),
    path(route='parameters/<uuid:pk>/update/', view=hospital_views.ParameterUpdate.as_view(), name='parameter-update'),
    path(route='parameters/<uuid:pk>/delete/', view=hospital_views.ParameterDelete.as_view(), name='parameter-delete'),

    path(route='patients_set/', view=hospital_views.manage_patients, name='patient-set'),
    path(route='patients/', view=hospital_views.PatientList.as_view(), name='patient-list'),
    path(route='patients/create/', view=hospital_views.PatientCreate.as_view(), name='patient-create'),
    path(route='patients/<uuid:pk>/update/', view=hospital_views.PatientUpdate.as_view(), name='patient-update'),
    path(route='patients/<uuid:pk>/delete/', view=hospital_views.PatientDelete.as_view(), name='patient-delete'),
]


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
