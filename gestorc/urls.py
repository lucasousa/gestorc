from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("core/", include("core.urls", namespace="core")),
    path("finance/", include("finance.urls", namespace="finance")),
]
