from django.urls import path

from .views import GuestSignUpView

urlpatterns = [
    path('guest-sign-up/', GuestSignUpView.as_view())
]
