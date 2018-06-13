from django.shortcuts import render
from django.utils.translation import pgettext_lazy


def permission_denied(request, exception):
    return render(
        request=request,
        template_name='hospital/error.html',
        context={
            'error_num': 403,
            'error_text': pgettext_lazy('error_msg', 'Forbidden'),
        },
    )
