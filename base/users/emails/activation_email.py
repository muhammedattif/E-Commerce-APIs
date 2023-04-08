# Django Imports
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

# Other Third Party Imports
from templated_mail.mail import BaseEmailMessage


class ActivationEmail(BaseEmailMessage):
    template_name = "users/activation_email_form.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = user.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["activation_url"] = settings.FRONT_END_ACTIVATION_URL.format(
            uid=user.encode_uid(user.pk),
            token=default_token_generator.make_token(user),
        )
        return context
