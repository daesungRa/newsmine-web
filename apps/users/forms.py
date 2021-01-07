from django.forms import Form, ValidationError
from django.forms import CharField, EmailField, PasswordInput

from apps.users.models import User as UserModel


class LoginForm(Form):
    """Login Form detail"""
    username = EmailField()
    password = CharField(widget=PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error('password', ValidationError('Password is wrong'))
        except UserModel.DoesNotExist as ne:
            self.add_error('username', ValidationError('User does not exist'))
