# Django Imports
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.db import transaction


class UserManager(BaseUserManager):
    """User Manager"""

    def create_user(self, email, password=None, is_staff=False, is_superuser=False, **kwargs):
        if not email:
            raise ValueError("User must have an email address")

        is_active = True
        if settings.SEND_ACTIVATION_EMAIL and not is_superuser:
            is_active = False

        user = self.model(
            email=self.normalize_email(email),
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    @transaction.atomic
    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        user.save(using=self._db)
        return user
