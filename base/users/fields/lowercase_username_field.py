# Django Imports
from django.db import models


class LowercaseUsernameField(models.CharField):
    """
    Override CharField to convert value to lowercase before saving.
    """

    def to_python(self, value):
        """
        Convert value to lowercase.
        """
        value = super(LowercaseUsernameField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value
