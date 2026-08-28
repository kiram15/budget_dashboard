"""
Plaid configuration, isolated from the rest of settings.py so it's
obvious at a glance what's Plaid-specific.

In your main config/settings.py, add:

    from .plaid_settings import *  # noqa
"""
import environ

env = environ.Env()
environ.Env.read_env()  # reads .env in project root

PLAID_CLIENT_ID = env("PLAID_CLIENT_ID")
PLAID_SECRET = env("PLAID_SECRET")
PLAID_ENV = env("PLAID_ENV", default="sandbox")  # sandbox | development | production
PLAID_REDIRECT_URI = env("PLAID_REDIRECT_URI", default="")

# Products your app actually uses — keep this list minimal, Plaid
# bills/scopes by product. Add "liabilities" later if you want
# credit card APR/statement data too.
PLAID_PRODUCTS = ["transactions", "investments"]
PLAID_COUNTRY_CODES = ["US"]

# Name under which all tokens are namespaced in the OS keychain.
# See apps/plaid_integration/token_store.py
KEYCHAIN_SERVICE_NAME = "budget-app"
