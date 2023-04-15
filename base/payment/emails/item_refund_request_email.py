# Other Third Party Imports
from templated_mail.mail import BaseEmailMessage

# First Party Imports
from base.utility.functions import build_backend_absolute_uri


class ItemRefundRequestEmail(BaseEmailMessage):
    template_name = "orders/emails/item_refund_request_form.html"

    def get_context_data(self):
        # Django Imports
        from django.contrib.sites.models import Site

        context = super().get_context_data()
        current_site = Site.objects.get_current().domain
        context["domain"] = current_site
        endpoint = "/ar/admin/orders/orderitemrefundrequest/{0}/change/".format(
            context.get("instance").id,
        )
        context["object_url"] = build_backend_absolute_uri(endpoint=endpoint)
        return context
