from rest_framework.generics import ListAPIView

from .models import Account
from .serializers import AccountSerializer


class AccountListView(ListAPIView):
    """
    GET /api/accounts/

    All linked accounts across every institution — generic on purpose
    (per project discussion: single-user app, Fidelity is currently the
    only investment account, so no institution filter yet). Add
    `?institution=` filtering later only if/when a second brokerage or
    bank gets linked and something actually needs to narrow it down.
    """

    serializer_class = AccountSerializer

    def get_queryset(self):
        # select_related walks Account -> PlaidItem -> Institution in one
        # query instead of one extra query per account for the
        # `institution` field in the serializer.
        return Account.objects.select_related("item__institution").all()
