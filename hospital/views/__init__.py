from django.template.defaultfilters import register

from . import profile, applications, forms, home, parameters, patients, projects, history_and_form, session_settings


@register.filter(name='correctDateFormat')
def correctDateFormat(value):
    # arg is optional and not needed but you could supply your own formatting if you want.
    dateformatted = value.strftime("%d.%m.%Y %H:%M:%S")
    return dateformatted
