from django.db.models import Model, DateTimeField


class TimeStampedModel(Model):

    """
    Custom TimeStamped Model
        disc: This is abstract model.
        It'll be implemented by applications in this project.
    """

    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = (
            '-created',
            '-updated',
        )
