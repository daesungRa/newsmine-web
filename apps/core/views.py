from django.shortcuts import render

from django.views.generic import View


def home_view(request):
    context = {}
    return render(request, 'home.html', context)
