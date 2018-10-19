from datetime import datetime

from company.models import Company
from financial_report.models import FinancialReport, FinancialData, FinancialRatio


def create_financial_report(
        company: Company,
        date_time: datetime,
) -> FinancialReport:
    financial_report = FinancialReport.objects.create(
        company_id=company.id,
        date_time=date_time,
        currency='SGD'
    )
    print(
        f'        + Financial Report \'{financial_report.id}\' ({financial_report.date_time}) created', )
    return financial_report


def create_financial_data(financial_report: FinancialReport, name: str, value: float, ) -> FinancialData:
    return financial_report.financial_data.create(name=name, value=value, )


def create_financial_ratio(financial_report: FinancialReport, name: str, value: float, ) -> FinancialRatio:
    return financial_report.financial_ratios.create(name=name, value=value, )
