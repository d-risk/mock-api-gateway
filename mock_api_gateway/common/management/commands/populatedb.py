from django.core.management.base import BaseCommand

from mock_api_gateway.common.management.commands._randomize import create_companies
from mock_api_gateway.common.management.commands._singtel import create_singtel_company

COMPANIES = 'companies'
# REPORTS = 'reports'
SINGTEL = 'singtel'


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(f'--{COMPANIES}', type=int, )
        # parser.add_argument(f'--{REPORTS}', type=int, )
        parser.add_argument(f'--{SINGTEL}', action='store_true', )

    def handle(self, *args, **options):
        companies: int = options[COMPANIES]
        # reports: int = options[REPORTS]
        if companies:
            create_companies(companies, 2010, 2018)
        if options[SINGTEL]:
            create_singtel_company()
