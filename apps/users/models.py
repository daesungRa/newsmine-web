from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Default User Model"""

    def __str__(self):
        return self.username
