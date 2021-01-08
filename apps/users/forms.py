from django.forms import Form, ModelForm, ValidationError
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


class SignUpForm(ModelForm):
    """Signup Form detail"""
    password = CharField(widget=PasswordInput)
    password_confirm = CharField(widget=PasswordInput, label='Confirm Password')

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            UserModel.objects.get(username=username)
            raise ValidationError('User already exists with that username/email')
        except UserModel.DoesNotExist:
            return username

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError('Password confirmation does not match')
        else:
            return password

    def save(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = super().save(commit=False)
        user.username = username
        user.set_password(password)
        user.email = username
        user.save()
