from django.shortcuts import render


def get_profile(request):
    return render(request, 'home/profile.html')
