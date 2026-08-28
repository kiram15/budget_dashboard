"""
Access-token storage via the OS keychain (macOS Keychain / Secret Service
on Linux / Windows Credential Locker — `keyring` picks the right backend
automatically).

Why this file exists and why it's small on purpose:
Plaid access tokens are the one piece of data in this whole app that could
actually be misused if leaked (they let someone pull fresh transaction data
for as long as the Item stays linked). Everything else in the database —
balances, transaction history, holdings — is just a read-only historical
record. Keeping ALL token access funneled through these two functions means
there's exactly one place to audit, and it's obvious from the code review
that PlaidItem.keychain_ref is a *name*, never a *secret*.
"""
import keyring

from config.plaid_settings import KEYCHAIN_SERVICE_NAME


def store_access_token(keychain_ref: str, access_token: str) -> None:
    keyring.set_password(KEYCHAIN_SERVICE_NAME, keychain_ref, access_token)


def get_access_token(keychain_ref: str) -> str | None:
    return keyring.get_password(KEYCHAIN_SERVICE_NAME, keychain_ref)


def delete_access_token(keychain_ref: str) -> None:
    """Call this when you unlink an institution — don't leave orphaned tokens."""
    try:
        keyring.delete_password(KEYCHAIN_SERVICE_NAME, keychain_ref)
    except keyring.errors.PasswordDeleteError:
        pass  # already gone, fine


def make_keychain_ref(institution_name: str, account_label: str) -> str:
    """
    Consistent naming so keychain entries stay legible if you ever open
    Keychain Access.app directly, e.g. "plaid_access_token_chase_checking".
    """
    slug = lambda s: s.lower().replace(" ", "_")
    return f"plaid_access_token_{slug(institution_name)}_{slug(account_label)}"
