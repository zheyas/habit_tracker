from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    telegram_chat_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telegram Chat ID'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # нужно оставить username для совместимости

    def __str__(self):
        return self.email
