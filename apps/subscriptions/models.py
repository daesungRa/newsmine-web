from django.db.models import CharField, TextField, BooleanField, IntegerField
from django.db.models import ForeignKey, ManyToManyField, CASCADE, SET_NULL

from django.core.validators import RegexValidator

from apps.core.models import TimeStampedModel
from apps.users.models import User as UserModel

CRON_REGEX = RegexValidator(
    regex="^{0}\\s+{1}\\s+{2}\\s+{3}\\s+{4}$".format(
        "(?P<minute>\\*|[0-5]?\\d)",
        "(?P<hour>\\*|[01]?\\d|2[0-3])",
        "(?P<day>\\*|0?[1-9]|[12]\\d|3[01])",
        "(?P<month>\\*|0?[1-9]|1[012])",
        "(?P<day_of_week>\\*|[0-6](\\-[0-6])?)",
    ),  # Reference by "https://gist.github.com/harshithjv/c58f0dfce0656cf94c8c"
    message='Only valid cron tab is required.'
)
CRON_TIME_REGEX = RegexValidator(
    regex="{0}\\s+{1}$".format(
        "(?P<minute>\\*|[0-5]?\\d)",
        "(?P<hour>\\*|[01]?\\d|2[0-3])",
    ),
    message='Only hour and minute fields are required.'
)


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


class CronTime(AbstractItem):
    """Schedule by Subscription Cron Time"""
    name = CharField(max_length=5, validators=[CRON_TIME_REGEX])


class Subscription(TimeStampedModel):
    """Default Subscription Model"""
    name = CharField(max_length=80)
    owner = ForeignKey(UserModel, related_name='subscriptions', on_delete=CASCADE)
    cron_time = ForeignKey(CronTime, related_name='subscriptions', on_delete=SET_NULL, null=True)
    cron = CharField(max_length=50, validators=[CRON_REGEX])
    keywords = ManyToManyField(Keyword, related_name='subscriptions', blank=True)
    exclusions = ManyToManyField(Exclusion, related_name='subscriptions', blank=True)
    labels = ManyToManyField(Label, related_name='subscriptions', blank=True)
    description = TextField(blank=True)
    display_count = IntegerField(default=10)
    active = BooleanField(default=False)
    send_count = IntegerField()
