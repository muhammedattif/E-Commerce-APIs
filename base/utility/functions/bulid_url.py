# Django Imports
from django.conf import settings


def build_absolute_uri(domain, endpoint):
    """buld absolute uri"""
    schema = "https"

    if not endpoint.startswith("/"):
        endpoint = f"/{endpoint}"

    return f"{schema}://{domain}{endpoint}"


def build_frontend_absolute_uri(endpoint):
    """buld absolute uri for front-end website"""

    return build_absolute_uri(domain=settings.FRONT_END_DOMAIN, endpoint=endpoint)


def build_backend_absolute_uri(endpoint):
    """buld absolute uri for back-end server"""

    return build_absolute_uri(domain=settings.BACK_END_DOMAIN, endpoint=endpoint)
