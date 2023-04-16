# REST Framework Imports
from rest_framework.routers import SimpleRouter

from .views import v1

seller_router_v1 = SimpleRouter(trailing_slash=False)
seller_router_v1.register(r"", v1.SellerViewSet, basename="seller")
