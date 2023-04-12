# REST Framework Imports
from rest_framework import status, viewsets
from rest_framework.response import Response

# First Party Imports
from base.utility.choices import Languages
from base.utility.classes import Requests
from base.utility.models import City
from base.utility.response_codes import GeneralCodes
from base.utility.serializers import CitySerializer


class CityViewSet(viewsets.GenericViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = City.objects.filter(is_active=True)
    serializer_class = CitySerializer
    pagination_class = None

    def get_queryset(self):
        governorate_id = self.request.query_params.get("governorate_id", None)
        lang = Requests.get_language(self.request)
        order_by = "en_name" if lang == Languages.EN else "ar_name"
        return self.queryset.filter(governorate_id=governorate_id).order_by(order_by)

    def get_serializer_context(self):
        context = super(CityViewSet, self).get_serializer_context()
        context.update({"lang": Requests.get_language(self.request)})
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
