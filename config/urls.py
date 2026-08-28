from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("plaid/", include("apps.plaid_integration.urls")),
]
