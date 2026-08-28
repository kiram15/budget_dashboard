"""
One shared, configured Plaid client. Import `plaid_client` everywhere else
in this app rather than constructing your own — keeps environment/credential
config in exactly one place.
"""
import plaid
from plaid.api import plaid_api

from django.conf import settings

_ENV_HOSTS = {
    "sandbox": plaid.Environment.Sandbox,
    "development": plaid.Environment.Development,
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
