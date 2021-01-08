import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from django.db.models import CharField, EmailField, ImageField, TextField, BooleanField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Default User Model"""
    LANG_ENG = 'eng'
    LANG_KOR = 'kor'
    LANG_CHOICES = ((LANG_ENG, 'Eng'), (LANG_KOR, 'Kor'),)

    LOGIN_EMAIL = 'email'
    LOGIN_GITHUB = 'github'
    LOGIN_GOOGLE = 'google'
    LOGIN_KAKAO = 'kakao'
    LOGIN_CHOICES = (
        (LOGIN_EMAIL, 'Email'),
        (LOGIN_GITHUB, 'Github'),
        (LOGIN_GOOGLE, 'Google'),
        (LOGIN_KAKAO, 'Kakao')
    )

    username = EmailField(
        unique=True,
        blank=False,
        # help_text='Required. email form only.',
        error_messages={'unique': 'A user with that username already exists.'},
    )

    nickname = CharField(max_length=150, blank=True)
    bio = TextField(blank=True)
    profile_image = ImageField(upload_to='profile_image', blank=True)

    language = CharField(max_length=3, choices=LANG_CHOICES, default=LANG_KOR, blank=True)
    superuser = BooleanField(default=False)

    email_verified = BooleanField(default=False)
    email_secret = CharField(max_length=120, default='', blank=True)
    login_method = CharField(max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)

    def __str__(self):
        return self.username

    def verify_email(self):
        if not self.email_verified:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_content = render_to_string('emails/verify_email.html', {'secret': secret})
            send_mail(
                'Verify Newsmine Account',
                strip_tags(f'{html_content} (secret: {secret})'),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=f'{html_content} (secret: {secret})'
            )
            self.save()
        return
