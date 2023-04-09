# First Party Imports
from base.utility.response_codes import GeneralCodes


class ErrorHandledSerializerMixin(object):
    """ErrorHandledSerializerMixin class"""

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception=raise_exception)
        if not is_valid and not hasattr(self, "code"):
            self.code = GeneralCodes.INVALID_DATA
        elif is_valid:
            self.code = GeneralCodes.SUCCESS

        return is_valid
