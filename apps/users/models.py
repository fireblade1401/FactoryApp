from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


def generate_telegram_token():
    return str(uuid.uuid4())


class CustomUser(AbstractUser):
    telegram_token = models.CharField(max_length=100, null=True, blank=True, default=generate_telegram_token)
    telegram_chat_id = models.IntegerField(null=True, blank=True)
