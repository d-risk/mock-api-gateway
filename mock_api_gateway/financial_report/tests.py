from uuid import uuid4

from django.test import TestCase
from django.utils.timezone import now

from mock_api_gateway.financial_report.models import FinancialReport


# Create your tests here.
class FinancialReportTestCase(TestCase):
    def test_create_financial_report(self):
        company_id = uuid4()
        date_time = now()
        currency = 'CR'

        financial_report = FinancialReport.objects.create(
            company_id=company_id,
            date_time=date_time,
            currency=currency,
        )

        self.assertEqual(FinancialReport.objects.count(), 1)
        self.assertIsNotNone(financial_report)
        self.assertEqual(financial_report.company_id, company_id)
        self.assertEqual(financial_report.date_time, date_time)
        self.assertEqual(financial_report.currency, currency)
