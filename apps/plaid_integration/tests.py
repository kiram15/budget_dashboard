from django.conf import settings
from django.test import TestCase


class PlaidProductSettingsTests(TestCase):
    def test_investment_and_transaction_products_are_enabled(self):
        self.assertEqual(
            [product.value for product in settings.PLAID_PRODUCTS],
            ["investments", "transactions"],
        )
