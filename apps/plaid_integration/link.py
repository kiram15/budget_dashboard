"""
The Plaid Link handshake, in two halves:

1. create_link_token()   — called BEFORE the widget opens, gives the
   frontend a short-lived token to initialize Plaid's hosted UI.
2. exchange_public_token() — called AFTER the widget succeeds, trades
   the temporary public_token for a real, long-lived access_token.

At no point does either function, or anything in this file, see a bank
username or password — that only ever exists inside Plaid's own widget.

MOVED from the nested apps/plaid_integration/plaid_integration/ duplicate —
see client.py's docstring for why. No logic changed.
"""
from django.conf import settings
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request_update import LinkTokenCreateRequestUpdate

from apps.accounts.models import Institution, PlaidItem
from .client import plaid_client
from .token_store import store_access_token, make_keychain_ref


def create_link_token(user_id: str = "local-user") -> str:
    """Step 1: get a link_token to hand to the frontend Link widget."""
    request = LinkTokenCreateRequest(
        products=settings.PLAID_PRODUCTS,
        client_name="Personal Budget App",
        country_codes=settings.PLAID_COUNTRY_CODES,
        language="en",
        user=LinkTokenCreateRequestUser(client_user_id=user_id),
        redirect_uri=settings.PLAID_REDIRECT_URI or None,
    )
    response = plaid_client.link_token_create(request)
    return response.link_token


def create_update_link_token(item: PlaidItem, user_id: str = "local-user") -> str:
    """
    Step 1, reauth variant: use when an Item's status is 'needs_reauth'
    (e.g. the institution forced a password reset). Reuses the existing
    Item so transaction/investment history isn't lost.
    """
    from .token_store import get_access_token

    access_token = get_access_token(item.keychain_ref)
    request = LinkTokenCreateRequest(
        products=[],  # empty for update mode
        client_name="Personal Budget App",
        country_codes=settings.PLAID_COUNTRY_CODES,
        language="en",
        user=LinkTokenCreateRequestUser(client_user_id=user_id),
        access_token=access_token,
        update=LinkTokenCreateRequestUpdate(),
    )
    response = plaid_client.link_token_create(request)
    return response.link_token


def exchange_public_token(
    public_token: str, institution_name: str, institution_plaid_id: str, account_label: str
) -> PlaidItem:
    """Step 2: trade the widget's temporary token for a real access token."""
    exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
    exchange_response = plaid_client.item_public_token_exchange(exchange_request)

    access_token = exchange_response.access_token
    item_id = exchange_response.item_id

    institution, _ = Institution.objects.get_or_create(
        plaid_institution_id=institution_plaid_id, defaults={"name": institution_name}
    )

    keychain_ref = make_keychain_ref(institution_name, account_label)
    store_access_token(keychain_ref, access_token)

    plaid_item = PlaidItem.objects.create(
        institution=institution, item_id=item_id, keychain_ref=keychain_ref
    )
    return plaid_item
