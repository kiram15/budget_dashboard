from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("plaid/", include("apps.plaid_integration.urls")),
    # New: read endpoints the frontend's api/client.js now calls instead
    # of mockData.js. Namespaced per-app rather than one flat api/urls.py,
    # so this stays easy to extend as transactions/spending views land.
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/investments/", include("apps.investments.urls")),
]
