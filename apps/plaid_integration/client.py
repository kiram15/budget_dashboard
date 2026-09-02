"""
One shared, configured Plaid client. Import `plaid_client` everywhere else
in this app rather than constructing your own — keeps environment/credential
config in exactly one place.

MOVED: this used to live at apps/plaid_integration/plaid_integration/client.py
(a nested duplicate package). config/urls.py already pointed at
"apps.plaid_integration.urls" — the non-nested path — so that nested copy
was dead code; INSTALLED_APPS registers "apps.plaid_integration", and
Django never executed anything under the inner plaid_integration/ folder.
Consolidated here so there's one copy, matching what was actually wired up.
"""
import plaid
from plaid.api import plaid_api

from django.conf import settings

_ENV_HOSTS = {
    "sandbox": plaid.Environment.Sandbox,
    "production": plaid.Environment.Production,
}


def _build_client() -> plaid_api.PlaidApi:
    configuration = plaid.Configuration(
        host=_ENV_HOSTS[settings.PLAID_ENV],
        api_key={
            "clientId": settings.PLAID_CLIENT_ID,
            "secret": settings.PLAID_SECRET,
        },
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)


plaid_client = _build_client()
