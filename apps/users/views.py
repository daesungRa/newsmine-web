import json
import requests

from django.views import View
from django.views.generic import FormView

from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy

from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout

from apps.users.models import User as UserModel
from apps.users.forms import LoginForm, SignUpForm

from config import CONFIG

GITHUB_CLIENT_ID = CONFIG['SOCIAL']['github.id']
GITHUB_CLIENT_SECRET = CONFIG['SOCIAL']['github.secret']
GITHUB_REDIRECT_URI = f'{CONFIG["HOST"]["url"]}/users/login/github/callback'
KAKAO_CLIENT_ID = CONFIG['SOCIAL']['kakao.id']
KAKAO_REDIRECT_URI = f'{CONFIG["HOST"]["url"]}/users/login/kakao/callback'


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
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = UserModel.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ''
        user.save()
        # TODO: Add success message
    except UserModel.DoesNotExist:
        # TODO: Add error message
        pass
    return redirect(reverse('core:home'))


class GithubException(Exception):
    pass


def github_login(request):
    scope = 'read:user'
    return redirect(
        f'https://github.com/login/oauth/authorize?'
        f'client_id={GITHUB_CLIENT_ID}&'
        f'redirect_uri={GITHUB_REDIRECT_URI}&'
        f'scope={scope}'
    )


def github_callback(request):
    try:
        code = request.GET.get('code', None)
        if code is not None:
            # Get access_token
            token_url = f'https://github.com/login/oauth/access_token?' \
                        f'client_id={GITHUB_CLIENT_ID}&' \
                        f'client_secret={GITHUB_CLIENT_SECRET}&' \
                        f'code={code}'
            token_response = requests.post(
                url=token_url,
                headers={'Accept': 'application/json'},
            )
            token_json = token_response.json()
            error = token_json.get('error', None)
            if error is not None:
                # TODO: Add error message of access token
                raise GithubException()
            access_token = token_json.get('access_token')
            # Get user info
            profile_response = requests.get(
                url='https://api.github.com/user',
                headers={
                    'Authorization': f'token {access_token}',
                    'Accept': 'application/json',
                },
            )
            profile_json = profile_response.json()
            username = profile_json.get('login', None)
            if username is not None:
                email = profile_json.get('email', None)
                if email is not None:
                    split_email = str.split(email, '@')
                    email = f'{split_email[0].lower()}@{split_email[1]}'
                else:
                    # TODO: Go to another email authentication
                    message = f'[EMAIL-NONE] Email not shown. ' \
                              f'Please set your public email in github.'
                    raise GithubException(message)
                name = profile_json.get('name', None)
                if not name:
                    name = name.split(' ')
                else:
                    name = ['NO_NAME']
                bio = profile_json.get('bio')
                # User existing check
                try:
                    user = UserModel.objects.get(username=email)
                    if user.login_method != UserModel.LOGIN_GITHUB:
                        # TODO: Add error message
                        raise GithubException()
                except UserModel.DoesNotExist:
                    # Create new user object
                    user = UserModel.objects.create(
                        username=email,
                        first_name=name[0],
                        last_name=len(name) > 1 and name[1] or '',
                        email=email,
                        bio=bio,
                        email_verified=True,
                        login_method=UserModel.LOGIN_GITHUB,
                    )
                    user.set_unusable_password()
                    user.save()
                # Trying to log in
                django_login(request, user)
                return redirect(reverse('core:home'))
            else:
                # TODO: Add error message of username not found
                raise GithubException()
        else:
            # TODO: Add code error from GITHUB_REDIRECT_URI
            raise GithubException()
    except GithubException as ge:
        # TODO: Send error message
        return redirect(reverse('users:login'))


class KakaoException(Exception):
    pass
