from uuid import uuid4

from django.test import TestCase
from django.utils.timezone import now

from credit_report.models import CreditReport


# Create your tests here.
class CreditReportTestCase(TestCase):
    def test_create_credit_report(self):
        company_id = uuid4()
        probability_of_default = 0.1
        credit_rating = 'CR'
        date_time = now()

        credit_report = CreditReport.objects.create(
            company_id=company_id,
            probability_of_default=probability_of_default,
            credit_rating=credit_rating,
            date_time=date_time,
        )

        self.assertEqual(CreditReport.objects.count(), 1)
        self.assertIsNotNone(credit_report)
        self.assertEqual(credit_report.company_id, company_id)
        self.assertEqual(credit_report.probability_of_default, probability_of_default)
        self.assertEqual(credit_report.date_time, date_time)
        self.assertIsNotNone(credit_report.financial_reports)
        self.assertEqual(credit_report.financial_reports.count(), 0)
        self.assertIsNotNone(credit_report.news)
        self.assertEqual(credit_report.news.count(), 0)
