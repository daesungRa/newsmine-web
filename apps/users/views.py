import json
import requests
from datetime import datetime, timezone

from django.views import View
from django.views.generic import FormView

from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.core.files.base import ContentFile

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout

from apps.users.models import User as UserModel
from apps.users.forms import LoginForm, SignUpForm

from config import CONFIG

GITHUB_CLIENT_ID = CONFIG['SOCIAL']['github.id']
GITHUB_CLIENT_SECRET = CONFIG['SOCIAL']['github.secret']
GITHUB_REDIRECT_URL = f'{CONFIG["HOST"]["url"]}/users/login/github/callback'
KAKAO_CLIENT_ID = CONFIG['SOCIAL']['kakao.id']
KAKAO_CLIENT_SECRET = CONFIG['SOCIAL']['kakao.secret']
KAKAO_REDIRECT_URL = f'{CONFIG["HOST"]["url"]}/users/login/kakao/callback'


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
        f'redirect_uri={GITHUB_REDIRECT_URL}&'
        f'scope={scope}'
    )


def github_callback(request):
    message_type = messages.ERROR
    return_message = '[SOCIAL-LOGIN] Fail to get github login page. Please try another way.'
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
                message_type = messages.ERROR
                return_message = '[SOCIAL-LOGIN] An error occurred while getting the github token.'
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
                    message_type = messages.WARNING
                    return_message = f'[SOCIAL-LOGIN] Email not shown. Please set your email public in github.'
                    raise GithubException()
                name = profile_json.get('name', None)
                if name:
                    name = name.split(' ')
                else:
                    name = ['NO_NAME']
                bio = profile_json.get('bio', None)
                avatar_url = profile_json.get('avatar_url', None)
                # User existing check
                try:
                    user = UserModel.objects.get(username=email)
                    if user.login_method != UserModel.LOGIN_GITHUB:
                        message_type = messages.WARNING
                        return_message = f'[SOCIAL-LOGIN] The user already exists. ({email})'
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
                message_type = messages.WARNING
                return_message = '[SOCIAL-LOGIN] Cannot find login username from github.'
                raise GithubException()
        else:
            message_type = messages.ERROR
            return_message = '[SOCIAL-LOGIN] Redirection code not found from github.'
            raise GithubException()
    except GithubException as ge:
        messages.add_message(request, message_type, return_message)
        return redirect(reverse('core:home'))


class KakaoException(Exception):
    pass


def kakao_login(request):
    return redirect(
        f'https://kauth.kakao.com/oauth/authorize?'
        f'client_id={KAKAO_CLIENT_ID}&'
        f'redirect_uri={KAKAO_REDIRECT_URL}&'
        f'response_type=code'
    )


def kakao_callback(request):
    message_type = messages.ERROR
    return_message = '[SOCIAL-LOGIN] Fail to get kakao login page. Please try another way.'
    try:
        code = request.GET.get('code', None)
        if code is not None:
            # Get access_token
            token_url = f'https://kauth.kakao.com/oauth/token?' \
                        f'grant_type=authorization_code&' \
                        f'client_id={KAKAO_CLIENT_ID}&' \
                        f'client_secret={KAKAO_CLIENT_SECRET}&' \
                        f'redirect_uri={KAKAO_REDIRECT_URL}&' \
                        f'code={code}'
            token_response = requests.post(url=token_url)
            token_json = token_response.json()
            # Error check
            error = token_json.get('error', None)
            if error is not None:
                message_type = messages.ERROR
                return_message = '[SOCIAL-LOGIN] An error occurred while getting the kakao token.'
                raise KakaoException()
            access_token = token_json.get('access_token', None)
            # Get user profile, email
            profile_response = requests.get(
                url='https://kapi.kakao.com/v2/user/me',
                headers={'Authorization': f'Bearer {access_token}'},
            )
            profile_json = profile_response.json()
            # Email existing check
            email = profile_json['kakao_account'].get('email', None)
            if email is not None:
                split_email = str.split(email, '@')
                email = f'{split_email[0].lower()}@{split_email[1]}'
            else:
                message_type = messages.WARNING
                return_message = f'[SOCIAL-LOGIN] Email not shown. Please set your email public in kakao.'
                raise KakaoException()
            properties = profile_json.get('properties', None)
            nickname = properties.get('nickname', None)
            if nickname:
                nickname = nickname.split(' ')
            else:
                nickname = ['NO_NAME']
            profile_image = properties.get('profile_image', None)
            thumbnail_image = properties.get('thumbnail_image', None)
            # User check and log in
            try:
                user = UserModel.objects.get(username=email)
                if user.login_method != UserModel.LOGIN_KAKAO:
                    message_type = messages.WARNING
                    return_message = f'[SOCIAL-LOGIN] The user already exists. ({email})'
                    raise KakaoException()
            except UserModel.DoesNotExist:
                user = UserModel.objects.create(
                    username=email,
                    first_name=nickname[0],
                    last_name=len(nickname) > 1 and nickname[1] or '',
                    email=email,
                    email_verified=True,
                    login_method=UserModel.LOGIN_KAKAO,
                )
                user.set_unusable_password()
                user.save()
                # Set user profile image
                if profile_image is not None:
                    photo_response = requests.get(profile_image)
                    # Handling bullshit file
                    user.profile_image.save(
                        f'{" ".join(nickname)}_{email}_profile_image_{datetime.now(tz=timezone.utc)}.png',
                        ContentFile(photo_response.content),
                    )
                if thumbnail_image is not None:
                    photo_response = requests.get(thumbnail_image)
                    # Handling bullshit file
                    user.thumbnail_image.save(
                        f'{" ".join(nickname)}_{email}_thumbnail_image_{datetime.now(tz=timezone.utc)}.png',
                        ContentFile(photo_response.content),
                    )
            django_login(request, user)
            return redirect(reverse('core:home'))
        else:
            message_type = messages.ERROR
            return_message = '[SOCIAL-LOGIN] Redirection code not found from kakao.'
            raise KakaoException()
    except KakaoException as ke:
        messages.add_message(request, message_type, return_message)
        return redirect(reverse('core:home'))
