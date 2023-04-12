# REST Framework Imports
from rest_framework.routers import SimpleRouter

from .views import v1

users_router_v1 = SimpleRouter(trailing_slash=False)
# users_router_v1.register(r"signup", v1.SignUpViewSet, basename="signup")
users_router_v1.register(r"auth", v1.AuthViewSet, basename="auth")
# users_router_v1.register(r"password-reset", v1.ResetPasswordViewSet, basename="reset-password")
users_router_v1.register(r"profile", v1.ProfileViewSet, basename="profile")
users_router_v1.register(r"addresses", v1.AddressViewSet, basename="addresses")
# users_router_v1.register(r"email-verification", v1.ResetPasswordViewSet, basename="email-verification")
