# Other Third Party Imports
from templated_mail.mail import BaseEmailMessage


class ConfirmationEmail(BaseEmailMessage):
    template_name = "users/confirmation_email_form.html"
