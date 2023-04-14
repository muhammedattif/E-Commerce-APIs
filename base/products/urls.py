# REST Framework Imports
from rest_framework.routers import SimpleRouter

from .views import v1

products_router_v1 = SimpleRouter(trailing_slash=False)
products_router_v1.register(r"", v1.ProductViewSet, basename="products")
products_router_v1.register(r"system-features", v1.SysFeaturesViewSet, basename="system-features")
