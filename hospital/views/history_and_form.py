from django.shortcuts import render


def manage_view(request):
    return render(request, 'hospital/history_and_form.html')
