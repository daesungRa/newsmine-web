from django.db.models import CharField, TextField, BooleanField, IntegerField
from django.db.models import ForeignKey, ManyToManyField, CASCADE

from apps.core.models import TimeStampedModel
from apps.users.models import User as UserModel


class AbstractItem(TimeStampedModel):
    """Abstract Item Model"""
    name = CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Keyword(AbstractItem):
    """Custom Keyword Model"""
    class Meta:
        verbose_name_plural = 'Keywords'
        ordering = ['name']


class Exclusion(AbstractItem):
    """Custom Exclusion Model"""
    class Meta:
        verbose_name_plural = 'Exclusions'
        ordering = ['name']


class Label(AbstractItem):
    """Custom Label Model"""
    class Meta:
        verbose_name_plural = 'Labels'
        ordering = ['name']


class Subscription(TimeStampedModel):
    """Default Subscription Model"""
    name = CharField(max_length=80)
    owner = ForeignKey(UserModel, related_name='subscriptions', on_delete=CASCADE)
    keywords = ManyToManyField(Keyword, related_name='subscriptions', blank=True)
    exclusions = ManyToManyField(Exclusion, related_name='subscriptions', blank=True)
    labels = ManyToManyField(Label, related_name='subscriptions', blank=True)
    description = TextField(blank=True)
    display_count = IntegerField(default=10)
    cron = CharField(max_length=10)
    active = BooleanField(default=False)
    send_count = IntegerField()
