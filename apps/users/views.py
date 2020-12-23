import json

from django.views import View

from django.shortcuts import render


class LoginView(View):
    """Custom Login View"""
    def get(self, request):
        form = 'ff'
        return render(request, 'account/login.html', {'form': form})
