# Python Standard Library Imports
from collections import OrderedDict

# REST Framework Imports
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# First Party Imports
from base.utility.response_codes import GeneralCodes


class CustomPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("code", GeneralCodes.SUCCESS),
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ],
            ),
        )
