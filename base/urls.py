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
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        # Debug tool Bar
        # TODO: To be added
        # Swagger
        # TODO: To be added
        # path('silk/', include('silk.urls', namespace='silk')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.index_title = settings.SITE_INDEX_TITLE
admin.site_title = settings.SITE_TITLE
admin.site_header = settings.SITE_HEADER
