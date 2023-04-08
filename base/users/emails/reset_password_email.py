# Django Imports
from django.urls import reverse

# Other Third Party Imports
from templated_mail.mail import BaseEmailMessage


class ResetPasswordEmail(BaseEmailMessage):
    template_name = "users/reset_password_email_form.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        token = context.get("token")
        domain = context.get("domain")
        protocol = context.get("protocol")
        context["current_user"] = user
        context["username"] = user.username
        context["email"] = user.email
        context["reset_password_url"] = "{protocol}://{domain}/{reset_endpoint}?token={token}".format(
            protocol=protocol,
            domain=domain,
            reset_endpoint=reverse("reset-password:reset-password-confirm"),
            token=token,
        )
        return context
