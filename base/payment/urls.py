# REST Framework Imports
from rest_framework.routers import SimpleRouter

from .views import v1

payment_router_v1 = SimpleRouter(trailing_slash=False)
payment_router_v1.register(r"cart", v1.CartViewSet, basename="cart")
payment_router_v1.register(r"orders", v1.OrderViewSet, basename="orders")
