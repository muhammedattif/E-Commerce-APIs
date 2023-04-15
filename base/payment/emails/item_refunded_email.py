# Other Third Party Imports
from templated_mail.mail import BaseEmailMessage


class ItemRefundedEmail(BaseEmailMessage):
    template_name = "orders/emails/item_refunded_form.html"

    def get_context_data(self):
        # Django Imports
        from django.contrib.sites.models import Site

        context = super().get_context_data()
        current_site = Site.objects.get_current().domain
        context["domain"] = current_site
        return context
