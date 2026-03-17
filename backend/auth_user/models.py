from django.conf import settings
from django.db import models


class BaseProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_profile",
    )
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class TgProfile(BaseProfile):
    tg_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return f"TG Profile: {self.tg_id}"


class WebProfile(BaseProfile):
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return f"Web Profile: {self.username}"
