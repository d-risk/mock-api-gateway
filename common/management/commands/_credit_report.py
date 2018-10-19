from datetime import datetime
from typing import List

from company.models import Company
from credit_report.models import CreditReport
from financial_report.models import FinancialReport


def create_credit_report(
        company: Company,
        probability_of_default: float,
        credit_rating: str,
        date_time: datetime,
        financial_reports: List[FinancialReport] = None,
) -> CreditReport:
    credit_report = CreditReport.objects.create(
        company_id=company.id,
        probability_of_default=probability_of_default,
        credit_rating=credit_rating,
        date_time=date_time,
    )
    if financial_reports:
        credit_report.financial_reports.set(financial_reports)
    print(f'        + Credit Report \'{credit_report.id}\' ({credit_report.date_time}) created', )
    return credit_report
