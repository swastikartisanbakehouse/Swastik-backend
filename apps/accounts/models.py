from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, default='')
    addresses = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
