from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registered = models.BooleanField()

    def __str__(self) -> str:
        return "User " + str(self.user.username)
