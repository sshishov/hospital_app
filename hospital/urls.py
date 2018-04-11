from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views import defaults as default_views

from . import views as hospital_views


urlpatterns = [
    url(regex=settings.ADMIN_URL, view=admin.site.urls),
    url(regex='^$', view=hospital_views.HomeView.as_view()),
    path('i18n/', include('django.conf.urls.i18n')),

    url(regex='^parameters_set/$', view=hospital_views.manage_parameters),
    path(route='parameters/', view=hospital_views.ParameterList.as_view(), name='parameter_list'),
    path(route='parameters/new/', view=hospital_views.ParameterCreate.as_view(), name='parameter_new'),
    path(route='parameters/<uuid:pk>/edit/', view=hospital_views.ParameterUpdate.as_view(), name='parameter_edit'),
    path(route='parameters/<uuid:pk>/delete/', view=hospital_views.ParameterDelete.as_view(), name='parameter_delete'),
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
