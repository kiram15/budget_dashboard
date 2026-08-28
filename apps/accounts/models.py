from django.db import models

class Institution(models.Model):
    """A bank/brokerage as Plaid identifies it (Chase, Fidelity, First Tech...)."""

    name = models.CharField(max_length=100)
    plaid_institution_id = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class PlaidItem(models.Model):
    """
    One Item = one successful Link session = one login at one institution.
    A single institution can have multiple Items if you ever re-link it
    (e.g. after a password change forces reauth).
    """

    STATUS_CHOICES = [
        ("active", "Active"),
        ("needs_reauth", "Needs reauth"),
        ("error", "Error"),
    ]

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    item_id = models.CharField(max_length=64, unique=True)  # from Plaid, not sensitive

    # IMPORTANT: this is a *reference name*, not the token itself.
    # The real access token lives only in the OS keychain — see
    # apps/plaid_integration/token_store.py. Never add an access_token
    # field to this model.
    keychain_ref = models.CharField(max_length=128, unique=True)

    cursor = models.CharField(max_length=256, blank=True)  # transactions/sync pagination
    last_synced_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.institution.name} ({self.status})"


class Account(models.Model):
    """A single checking/credit/brokerage account within a PlaidItem."""

    TYPE_CHOICES = [
        ("depository", "Depository"),
        ("credit", "Credit"),
        ("investment", "Investment"),
        ("loan", "Loan"),
    ]

    item = models.ForeignKey(PlaidItem, on_delete=models.CASCADE, related_name="accounts")
    plaid_account_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=100)  # "Chase Total Checking"
    official_name = models.CharField(max_length=150, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    subtype = models.CharField(max_length=30, blank=True)  # checking / credit card / brokerage
    mask = models.CharField(max_length=4, blank=True)  # last 4 digits, for display only

    current_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    available_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    iso_currency_code = models.CharField(max_length=3, default="USD")

    def __str__(self):
        suffix = f" ...{self.mask}" if self.mask else ""
        return f"{self.name}{suffix}"
