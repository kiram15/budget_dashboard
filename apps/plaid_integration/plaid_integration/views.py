import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from . import link, sync


def link_page(request):
    """Renders the page that embeds Plaid's Link widget. Run this locally
    (127.0.0.1 only — see ARCHITECTURE.md) whenever adding a new institution."""
    link_token = link.create_link_token()
    return render(request, "plaid_integration/link.html", {"link_token": link_token})


@csrf_exempt  # local single-user tool; add real auth before ever exposing this beyond 127.0.0.1
@require_POST
def exchange_token(request):
    """
    Called by the frontend after Link succeeds. Body:
    {
      "public_token": "...",
      "institution_name": "Chase",
      "institution_id": "ins_...",
      "account_label": "checking"   # your own short label, used in the keychain ref
    }
    """
    body = json.loads(request.body)
    item = link.exchange_public_token(
        public_token=body["public_token"],
        institution_name=body["institution_name"],
        institution_plaid_id=body["institution_id"],
        account_label=body.get("account_label", "default"),
    )
    accounts = sync.fetch_and_create_accounts(item)
    sync.sync_all(item)

    return JsonResponse(
        {
            "item_id": item.item_id,
            "keychain_ref": item.keychain_ref,
            "accounts": [a.name for a in accounts],
        }
    )


@require_POST
def sync_now(request, item_id):
    """Manual 'Sync Now' trigger for a single institution."""
    from apps.accounts.models import PlaidItem

    item = PlaidItem.objects.get(item_id=item_id)
    result = sync.sync_all(item)
    return JsonResponse(result)
