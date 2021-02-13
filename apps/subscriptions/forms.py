from django.forms import ModelForm, ValidationError
from django.forms import CharField

from apps.subscriptions.models import Subscription as SubscriptionModel


class SubscriptionForm(ModelForm):
    """Default Subscription Form"""
    class Meta:
        model = SubscriptionModel
        fields = [
            'name', 'keywords', 'exclusions', 'labels', 'description',
            'display_count', 'cron', 'active', 'send_count',
        ]

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if not name:
            raise ValidationError(f'Name must not be blank.')
        try:
            SubscriptionModel.objects.get(name=name)
            raise ValidationError(f'Name {name} already exists. Please enter another name')
        except SubscriptionModel.DoesNotExist:
            return name
