from datetime import datetime
from typing import List

from company.models import Company
from credit_report.models import CreditReport
from financial_report.models import FinancialReport
from news.models import News


def create_credit_report(
        company: Company,
        probability_of_default: float,
        credit_rating: str,
        date_time: datetime,
        financial_reports: List[FinancialReport] = None,
        news: List[News] = None,
) -> CreditReport:
    credit_report = CreditReport.objects.create(
        company_id=company.id,
        probability_of_default=probability_of_default,
        credit_rating=credit_rating,
        date_time=date_time,
    )
    if financial_reports:
        credit_report.financial_reports.set(financial_reports)
    if news:
        credit_report.news.set(news)
    print(f'        + Credit Report \'{credit_report.id}\' ({credit_report.date_time}) created', )
    return credit_report
