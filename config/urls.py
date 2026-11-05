from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("identities.api.urls")),
    path("api/v1/", include("catalog.api.urls")),
    path("api/v1/", include("commerce.api.urls")),
]

