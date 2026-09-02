"""
MOVED from the nested apps/plaid_integration/plaid_integration/management/
duplicate — see apps/plaid_integration/client.py's docstring for why.
No logic changed.
"""
from django.core.management.base import BaseCommand

from apps.accounts.models import PlaidItem
from apps.plaid_integration.sync import sync_all


class Command(BaseCommand):
    help = "Sync transactions and investments for one or all linked institutions."

    def add_arguments(self, parser):
        parser.add_argument(
            "--item", dest="item_id", help="Sync only this Item ID (see PlaidItem.item_id)"
        )

    def handle(self, *args, **options):
        items = PlaidItem.objects.filter(status="active")
        if options["item_id"]:
            items = items.filter(item_id=options["item_id"])

        if not items:
            self.stdout.write(self.style.WARNING("No active items to sync."))
            return

        for item in items:
            self.stdout.write(f"Syncing {item.institution.name}...")
            try:
                result = sync_all(item)
                self.stdout.write(self.style.SUCCESS(f"  {result}"))
            except Exception as exc:
                item.status = "error"
                item.save(update_fields=["status"])
                self.stdout.write(self.style.ERROR(f"  failed: {exc}"))
