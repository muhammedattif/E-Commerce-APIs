# REST Framework Imports
from rest_framework.routers import SimpleRouter

from .views import v1

categories_router_v1 = SimpleRouter(trailing_slash=False)
categories_router_v1.register(r"", v1.CategoryViewSet, basename="categories")
