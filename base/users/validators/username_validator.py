# Python Standard Library Imports
import re

# Django Imports
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    regex = r"^(?![_])(?![0-9_])(?!^\d+$)[a-zA-Z0-9_]+$"
    message = _(
        "Enter a valid username. This value may contain only English letters, Numbers and _ symbol without spaces.",
    )
    flags = re.ASCII
