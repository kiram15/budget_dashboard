"""
Everything here is designed to be safely re-run: call sync_all(item) as
often as you like (once a day, once a month, whatever you're actually
opening the app) — nothing here assumes a background daemon or webhooks.

MOVED from the nested apps/plaid_integration/plaid_integration/ duplicate —
see client.py's docstring for why. No logic changed. (Note: the
PortfolioHistoryView added in apps/investments/views.py now depends on
this file's habit of writing a fresh HoldingSnapshot on every sync — see
the comment there about de-duplicating same-day syncs.)
"""
from datetime import date, timedelta
from decimal import Decimal

from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest

from apps.accounts.models import Account, PlaidItem
from apps.investments.models import Security, Holding, InvestmentTransaction, HoldingSnapshot
from .client import plaid_client
from .token_store import get_access_token


def fetch_and_create_accounts(item: PlaidItem) -> list[Account]:
    """Run once, right after linking — pulls the account list for a new Item."""
    access_token = get_access_token(item.keychain_ref)
    response = plaid_client.accounts_get(AccountsGetRequest(access_token=access_token))

    accounts = []
    for acct in response.accounts:
        account, _ = Account.objects.update_or_create(
            plaid_account_id=acct.account_id,
            defaults=dict(
                item=item,
                name=acct.name,
                official_name=acct.official_name or "",
                type=acct.type.value,
                subtype=(acct.subtype.value if acct.subtype else ""),
                mask=acct.mask or "",
                current_balance=acct.balances.current,
                available_balance=acct.balances.available,
                iso_currency_code=acct.balances.iso_currency_code or "USD",
            ),
        )
        accounts.append(account)
    return accounts


def sync_investments(item: PlaidItem) -> None:
    """
    Investments have no cursor-based endpoint like transactions do — we
    re-fetch current holdings each time, and pull any new investment
    transactions from the last sync forward.
    """
    access_token = get_access_token(item.keychain_ref)

    holdings_response = plaid_client.investments_holdings_get(
        InvestmentsHoldingsGetRequest(access_token=access_token)
    )

    security_map = {}
    for sec in holdings_response.securities:
        security, _ = Security.objects.update_or_create(
            plaid_security_id=sec.security_id,
            defaults=dict(
                ticker_symbol=sec.ticker_symbol or "",
                cusip=sec.cusip or "",
                name=sec.name or "",
                security_type=sec.type or "other",
                close_price=sec.close_price,
                close_price_date=sec.close_price_as_of,
                iso_currency_code=sec.iso_currency_code or "USD",
            ),
        )
        security_map[sec.security_id] = security

        # Append today's price to history — this is how price history
        # accumulates going forward (see SecurityPriceHistory docstring).
        if sec.close_price and sec.close_price_as_of:
            from apps.investments.models import SecurityPriceHistory
            SecurityPriceHistory.objects.update_or_create(
                security=security,
                date=sec.close_price_as_of,
                defaults={"close_price": sec.close_price, "source": "plaid_sync"},
            )

    for h in holdings_response.holdings:
        account = Account.objects.get(plaid_account_id=h.account_id)
        security = security_map[h.security_id]
        holding, _ = Holding.objects.update_or_create(
            account=account,
            security=security,
            defaults=dict(
                quantity=Decimal(str(h.quantity)),
                cost_basis=h.cost_basis,
                institution_value=Decimal(str(h.institution_value)),
                institution_price_as_of=h.institution_price_as_of,
            ),
        )
        # Write today's snapshot for historical charting — see
        # HoldingSnapshot docstring for why this is separate from Holding.
        HoldingSnapshot.objects.create(
            account=account, security=security, quantity=holding.quantity,
            value=holding.institution_value,
        )

    start_date = item.last_synced_at.date() if item.last_synced_at else date.today() - timedelta(days=365)
    txns_response = plaid_client.investments_transactions_get(
        InvestmentsTransactionsGetRequest(
            access_token=access_token, start_date=start_date, end_date=date.today()
        )
    )
    for txn in txns_response.investment_transactions:
        account = Account.objects.get(plaid_account_id=txn.account_id)
        security = security_map.get(txn.security_id) if txn.security_id else None
        InvestmentTransaction.objects.update_or_create(
            plaid_investment_transaction_id=txn.investment_transaction_id,
            defaults=dict(
                account=account, security=security, date=txn.date, type=txn.type,
                subtype=txn.subtype or "", quantity=txn.quantity, price=txn.price,
                amount=Decimal(str(txn.amount)), fees=txn.fees,
            ),
        )


def sync_all(item: PlaidItem) -> dict:
    """The one function your management command / 'Sync Now' view calls."""
    if item.accounts.filter(type="investment").exists():
        sync_investments(item)
        return {"note": "investments synced; transaction sync is disabled"}
    return {"note": "no investment accounts on this item; nothing synced"}
