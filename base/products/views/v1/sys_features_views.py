# REST Framework Imports
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

# Other Third Party Imports
from django_filters.rest_framework import DjangoFilterBackend

# First Party Imports
from base.products.models import SysFeature
from base.products.serializers import SysFeatureSerializer
from base.users.authentication import CustomTokenAuthentication
from base.users.permissions import SellerPermission


class SysFeaturesViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [SellerPermission]

    queryset = SysFeature.objects.filter(is_active=True).order_by("-id")
    serializer_class = SysFeatureSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name"]
    filterset_fields = ["name"]
