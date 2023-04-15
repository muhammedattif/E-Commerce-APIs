# Django Imports
from django import forms

# First Party Imports
from base.utility.choices import ApprovalActionChoices, ApprovalRequestChoices
from base.utility.utility_admin.functions import render_alert


class AbstractApprovalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.request_type == ApprovalRequestChoices.UPDATION:
            updated_fields = self.instance.updated_fields.keys()
            message = None
            color = None
            if self.instance.action == ApprovalActionChoices.SUBMITTED:
                message = "This Field is Pending Approval."
                color = "orange"
            elif self.instance.action == ApprovalActionChoices.APPROVED:
                message = "Approved."
                color = "green"
            elif self.instance.action == ApprovalActionChoices.DECLINED:
                message = "Declined."
                color = "Red"

            if message:
                for field in updated_fields:
                    if field in self.fields:
                        if self.instance.action == ApprovalActionChoices.SUBMITTED:
                            old_value = getattr(self.instance.primary_instance, field)
                            old_value_text = render_alert(message=" Old Value is {0}".format(old_value), color="black")
                        self.fields[field].help_text = render_alert(message=message, color=color) + old_value_text
