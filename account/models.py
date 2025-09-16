from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets
from datetime import timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username

class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_keys")
    key = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField()
    active = models.BooleanField(default=True)

    @staticmethod
    def create_key(user, days_valid=5):
        key = secrets.token_hex(16)
        expires = timezone.now() + timedelta(days=days_valid)
        return APIKey.objects.create(user=user, key=key, expires=expires)
