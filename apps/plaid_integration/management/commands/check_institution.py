"""
MOVED from the nested apps/plaid_integration/plaid_integration/management/
duplicate — see apps/plaid_integration/client.py's docstring for why.
No logic changed.
"""
from django.core.management.base import BaseCommand
from plaid.model.institutions_search_request import InstitutionsSearchRequest

from apps.plaid_integration.client import plaid_client
from django.conf import settings


class Command(BaseCommand):
    help = "Search Plaid's institution directory before attempting to link a new one."

    def add_arguments(self, parser):
        parser.add_argument("name", help='Institution name to search, e.g. "First Tech"')

    def handle(self, *args, **options):
        response = plaid_client.institutions_search(
            InstitutionsSearchRequest(
                query=options["name"],
                products=settings.PLAID_PRODUCTS,
                country_codes=settings.PLAID_COUNTRY_CODES,
            )
        )
        if not response.institutions:
            self.stdout.write(self.style.WARNING("No matches found."))
            return

        for inst in response.institutions:
            self.stdout.write(f"{inst.name}  (id={inst.institution_id})")
            self.stdout.write(f"  oauth: {inst.oauth}")
