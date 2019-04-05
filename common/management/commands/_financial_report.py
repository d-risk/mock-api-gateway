from datetime import datetime, timezone
from random import randint, uniform
from typing import List, Dict

from company.models import Company
from financial_report.models import FinancialReport, FinancialData, FinancialRatio

REVENUE = 'Revenue'
EBIT = 'EBIT'
EBITDA = 'EBITDA'
INTEREST_EXPENSE = 'Interest Expense'
PROFIT_BEFORE_TAX = 'Profit Before Tax'
PROFIT_AFTER_TAX = 'Profit After Tax'
CASH_EQUIVALENTS = 'Cash and Cash Equivalents'
TOTAL_ASSETS = 'Total Assets'
TOTAL_LIABILITIES = 'Total Liabilities'
TOTAL_DEBT = 'Total Debt'
TOTAL_EQUITY = 'Total Equity'
CURRENT_ASSETS = 'Current Assets'
CURRENT_LIABILITIES = 'Current Liabilities'
FINANCIAL_DATA: List[str] = [
    REVENUE,
    EBIT,
    EBITDA,
    INTEREST_EXPENSE,
    PROFIT_BEFORE_TAX,
    PROFIT_AFTER_TAX,
    CASH_EQUIVALENTS,
    TOTAL_ASSETS,
    TOTAL_LIABILITIES,
    TOTAL_DEBT,
    TOTAL_EQUITY,
    CURRENT_ASSETS,
    CURRENT_LIABILITIES,
]

FINANCIAL_RATIOS: Dict[str, str] = {
    'Debt Cover': f'{EBITDA} / {INTEREST_EXPENSE}',
    'Size': f'ln({TOTAL_ASSETS})',
    'ROA': f'{PROFIT_AFTER_TAX} / {TOTAL_ASSETS}',
    'Quick Ratio': f'(Total Current Assets - Inventory) / Total Current Liabilities',
    'Liabilities over Total Assets': f'{TOTAL_LIABILITIES} / {TOTAL_ASSETS}',
    'ROE': f'Profit After Tax / Total Equity',
    'Leverage': f'(Total Debt - Cash) / {EBITDA}',
    'Current Ratio': f'Total Current Assets / Total Current Liabilities',
}


def create_financial_report(
        company: Company,
        date_time: datetime,
) -> FinancialReport:
    financial_report = FinancialReport.objects.create(
        company_id=company.company_id,
        date_time=date_time,
        currency='SGD'
    )
    print(f'        + Financial Report \'{financial_report.report_id}\' ({financial_report.date_time}) created', )
    return financial_report


def create_financial_data(financial_report: FinancialReport, name: str, value: float, ) -> FinancialData:
    return financial_report.financial_data.create(name=name, value=value, )


def create_financial_ratio(
        financial_report: FinancialReport,
        name: str,
        value: float,
        formula: str,
) -> FinancialRatio:
    return financial_report.financial_ratios.create(name=name, value=value, formula=formula, )


def random_financial_data(financial_report: FinancialReport):
    for name in FINANCIAL_DATA:
        create_financial_data(financial_report=financial_report, name=name, value=uniform(0, 999_999_999_999), )


def random_financial_ratio(financial_report: FinancialReport):
    for name, formula in FINANCIAL_RATIOS.items():
        create_financial_ratio(
            financial_report=financial_report,
            name=name,
            value=uniform(-999_999, 999_999),
            formula=formula,
        )


def random_financial_report(company: Company, date_time: datetime) -> FinancialReport:
    financial_report = create_financial_report(company=company, date_time=date_time)
    random_financial_data(financial_report=financial_report, )
    random_financial_ratio(financial_report=financial_report, )
    return financial_report


def random_financial_reports(company: Company, from_year: int, to_year: int) -> List[FinancialReport]:
    financial_reports: List[FinancialReport] = []
    for year in range(from_year, to_year + 1):
        date_time = datetime(year=year, month=randint(1, 12), day=randint(1, 28), tzinfo=timezone.utc, )
        financial_report = random_financial_report(company=company, date_time=date_time, )
        financial_reports.append(financial_report, )
        date_time = datetime(year=year, month=randint(1, 12), day=randint(1, 28), tzinfo=timezone.utc, )
        financial_report = random_financial_report(company=company, date_time=date_time, )
        financial_reports.append(financial_report, )
    return financial_reports
