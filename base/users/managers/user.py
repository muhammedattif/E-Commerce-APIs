# Django Imports
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.db import transaction


class UserManager(BaseUserManager):
    """User Manager"""

    def create_user(self, email, username, password=None, is_staff=False, is_superuser=False, **kwargs):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")

        is_active = True
        if settings.SEND_ACTIVATION_EMAIL and not is_superuser:
            is_active = False

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    @transaction.atomic
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            is_staff=True,
            is_superuser=True,
        )
        user.save(using=self._db)
        return user
