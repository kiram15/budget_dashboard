"""
MOVED from the nested apps/plaid_integration/plaid_integration/urls.py
duplicate. config/urls.py already referenced "apps.plaid_integration.urls"
(this path, not the nested one) via
    path("plaid/", include("apps.plaid_integration.urls"))
so this file existing here — rather than one level down — is what makes
the /plaid/link/, /plaid/link/exchange/, and /plaid/sync/<item_id>/
routes actually resolve.
"""
from django.urls import path

from . import views

app_name = "plaid_integration"

urlpatterns = [
    path("link/", views.link_page, name="link_page"),
    path("link/exchange/", views.exchange_token, name="exchange_token"),
    path("sync/<str:item_id>/", views.sync_now, name="sync_now"),
]
