# REST Framework Imports
from rest_framework.routers import SimpleRouter

from .views import v1

utilities_router_v1 = SimpleRouter(trailing_slash=False)
utilities_router_v1.register(r"", v1.GenericViewSet, basename="generic")
utilities_router_v1.register(r"governorates", v1.GovernorateViewSet, basename="governorates")
utilities_router_v1.register(r"cities", v1.CityViewSet, basename="cities")
