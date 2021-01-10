import json

from django.views import View
from django.views.generic import FormView

from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy

from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout

from apps.users.forms import LoginForm, SignUpForm


class LoginView(FormView):
    """Custom Login View"""
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            django_login(self.request, user)
        return super().form_valid(form)


def logout(request):
    django_logout(request)
    return redirect(reverse('core:home'))


class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('core:home')
    # initial = {
    #     'username': 'daesungra@gmail.com',
    #     'first_name': 'Daesung',
    #     'last_name': 'Ra',
    # }

    def form_valid(self, form):
        # create user after validation check
        # username same as email form
        form.save()

        # login action
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            django_login(self.request, user)
        # user.verify_email()
        return super().form_valid(form)
