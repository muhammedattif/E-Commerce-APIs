# REST Framework Imports
from rest_framework import mixins, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

# First Party Imports
from base.categories.models import Category
from base.categories.serializers import CategoryDetailSerializer, CategorySerializer
from base.users.authentication import TokenOrAnonymousAuthentication
from base.utility.response_codes import GeneralCodes


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    authentication_classes = [TokenOrAnonymousAuthentication]
    permission_classes = []

    queryset = Category.objects.filter(level=0, is_active=True).order_by("-id")
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def retrieve(self, request, pk, *args, **kwargs):
        instance = Category.objects.filter(pk=pk, is_active=True).first()
        if not instance:
            return Response(
                {
                    "code": GeneralCodes.NOT_FOUND,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CategoryDetailSerializer(instance, context={"request": request})
        # TODO: Add Category Tracker
        return Response(
            {
                "code": GeneralCodes.SUCCESS,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
