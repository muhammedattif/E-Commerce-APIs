"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Django Imports
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# First Party Imports
from base.brands.urls import brands_router_v1
from base.categories.urls import categories_router_v1
from base.payment.urls import payment_router_v1
from base.products.urls import products_router_v1
from base.sellers.urls import seller_router_v1
from base.users.urls import users_router_v1
from base.utility.urls import utilities_router_v1

urlpatterns = [
    path("admin/", admin.site.urls),
    # Users APIs v1
    path("api/users/v1/", include((users_router_v1.urls, "users"), namespace="users-apis-v1")),
    # Products APIs v1
    path("api/products/v1/", include((products_router_v1.urls, "products"), namespace="products-apis-v1")),
    path("products/autocomplete/", include("base.products.autocomplete_urls")),
    # Brands APIs v1
    path("api/brands/v1/", include((brands_router_v1.urls, "brands"), namespace="brands-apis-v1")),
    # Categories APIs v1
    path("api/categories/v1/", include((categories_router_v1.urls, "categories"), namespace="categories-apis-v1")),
    # payment APIs v1
    path("api/payment/v1/", include((payment_router_v1.urls, "payment"), namespace="payment-apis-v1")),
    # Utility APIs v1
    path("api/utilities/v1/", include((utilities_router_v1.urls, "utilities"), namespace="utilities-apis-v1")),
    # Seller APIs v1
    path("api/sellers/v1/", include((seller_router_v1.urls, "sellers"), namespace="sellers-apis-v1")),
]

if settings.DEBUG:
    urlpatterns += [
        # Debug tool Bar
        # TODO: To be added
        # Swagger
        # TODO: To be added
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.index_title = settings.SITE_INDEX_TITLE
admin.site_title = settings.SITE_TITLE
admin.site_header = settings.SITE_HEADER
