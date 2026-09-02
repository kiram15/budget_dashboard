from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    Shape matches frontend/src/api/mockData.js `accounts`:
    { id, name, type, institution, balance }

    `institution` and `balance` don't exist as direct fields on Account —
    institution is two hops away (Account -> PlaidItem -> Institution),
    and the frontend's "balance" is our current_balance. Keeping the
    renaming here, in the serializer, means the frontend never has to
    know our internal field names.
    """

    institution = serializers.CharField(source="item.institution.name", read_only=True)
    balance = serializers.DecimalField(
        source="current_balance", max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = Account
        fields = ["id", "name", "type", "institution", "balance"]

    # NOTE: Account.type uses Plaid's vocabulary (depository/credit/
    # investment/loan) but mockData.js used checking/savings/investment.
    # Not translating that here on purpose — flagging it instead, since
    # deciding whether the frontend should branch on Plaid's categories
    # directly or keep a friendlier label is a product call, not something
    # to silently paper over in a serializer.
