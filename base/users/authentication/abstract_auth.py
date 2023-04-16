# Django Imports
from django.utils.translation import gettext_lazy as _

# REST Framework Imports
from rest_framework import exceptions

# First Party Imports
from base.utility.response_codes import UsersCodes


class AbstractAuth:
    """
    Header based reset password authentication
    """

    keyword = "Token"
    check_user_login_eligibility = True

    def get_authorization_header(self, request):
        """
        Return request's 'Authorization:' header, as a bytestring.

        Hide some test client ickyness where the header can be unicode.
        """
        auth = request.META.get("HTTP_AUTHORIZATION", None)
        return auth

    def authenticate(self, request):
        """
        Authenticates a user.
        """
        auth = self.get_authorization_header(request)
        if not auth:
            msg = _(" No credentials provided.")
            raise exceptions.AuthenticationFailed(
                detail={
                    "message": msg,
                    "code": UsersCodes.NO_CREDENTIALS_PROVIDED,
                },
            )

        auth = auth.split()
        if auth[0].lower() != self.keyword.lower():
            msg = _("Invalid Header.")
            raise exceptions.AuthenticationFailed(
                detail={
                    "message": msg,
                    "code": UsersCodes.INVALID_HEADER,
                },
            )

        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise exceptions.AuthenticationFailed(
                detail={
                    "message": msg,
                    "code": UsersCodes.INVALID_HEADER,
                },
            )

        elif len(auth) > 2:
            msg = _("Invalid token header. Token string should not contain spaces.")
            raise exceptions.AuthenticationFailed(
                detail={
                    "message": msg,
                    "code": UsersCodes.INVALID_HEADER,
                },
            )

        key = auth[1]
        user, token = self.authenticate_credentials(key)
        if self.check_user_login_eligibility:
            self.check_user(user=user)
        return (user, token)

    def authenticate_credentials(self, key):
        """
        Authenticate the credentials.
        """
        raise NotImplementedError(".authenticate_credentials() must be overridden.")

    def authenticate_header(self, request):
        return self.keyword

    @staticmethod
    def check_user(user):
        """
        Check if User's Email Verification or Suspension
        """
        if not user.is_active:
            msg = _("User inactive or deleted.")
            raise exceptions.AuthenticationFailed(
                detail={
                    "message": msg,
                    "code": UsersCodes.INACTIVE,
                },
            )

        if user.is_suspended:
            msg = _("User has been temporarily blocked due to violating the rules.")
            raise exceptions.AuthenticationFailed(
                detail={
                    "message": msg,
                    "code": UsersCodes.SUSPENDED,
                },
            )

        if not user.is_email_verified:
            msg = _("User's email is not verified.")
            raise exceptions.AuthenticationFailed(
                detail={
                    "message": msg,
                    "code": UsersCodes.EMAIL_NOT_VERIFIED,
                },
            )
        return
