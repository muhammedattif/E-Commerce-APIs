# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Other Third Party Imports
from django_countries.fields import CountryField

# First Party Imports
from base.users.fields import LowercaseEmailField
from base.utility import AbstractModel


class Address(AbstractModel):
    """
    Address model
    """

    user = models.ForeignKey(
        "base.User",
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name=_("User"),
    )
    first_name = models.CharField(max_length=30, verbose_name=_("First name"))
    last_name = models.CharField(max_length=30, verbose_name=_("Last Name"))
    email = LowercaseEmailField(
        max_length=60,
        verbose_name=_("Email"),
    )
    governorate = models.ForeignKey(
        "base.Governorate",
        on_delete=models.CASCADE,
        max_length=30,
        verbose_name=_("Governorate"),
    )
    city = models.ForeignKey(
        "base.City",
        on_delete=models.CASCADE,
        max_length=30,
        verbose_name=_("City"),
    )
    street_1 = models.CharField(max_length=30, verbose_name=_("Streat 1"))
    street_2 = models.CharField(null=True, blank=True, max_length=30, verbose_name=_("Streat 2"))
    landmark = models.CharField(null=True, blank=True, max_length=30, verbose_name=_("Landmark"))
    phone_number = models.CharField(max_length=30, verbose_name=_("Phone Number"))
    country = CountryField(verbose_name=_("Country"))

    is_primary = models.BooleanField(default=False, verbose_name=_("Is Primary?"))

    class Meta:
        db_table = "users_addresses"
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return "{0}".format(self.user.email)

    def process_primary(self):
        """
        Process primary does for the following:
        1- If the address is primary --> Flag other addresses as is_primary = False
        2- If there is not Primary Addresses --> Flag it as is_primary = True
        """
        existing_primary_addresses = self.__class__.objects.filter(
            user=self.user,
            is_primary=True,
            is_active=True,
        ).exclude(
            id=self.id,
        )

        if not (self.is_primary or existing_primary_addresses):
            self.is_primary = True

        elif self.is_primary and existing_primary_addresses:
            existing_primary_addresses.update(is_primary=False)

        return True
