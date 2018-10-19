import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from random import randint, choice, uniform
from typing import List

from common.management.commands._company import create_company
from common.management.commands._credit_report import create_credit_report
from common.management.commands._financial_report import create_financial_report, create_financial_data, \
    create_financial_ratio
from company.models import Company
from financial_report.models import FinancialReport

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

RATINGS = [
    'AAA',
    'AA',
    'A',
    'BBB',
    'BB',
    'B',
    'CCC',
    'CC',
    'C',
]

NOUN_LIST_URL = 'http://www.desiquintans.com/downloads/nounlist/nounlist.txt'
NOUN_LIST_FILENAME = 'noun_list.txt'

FINANCIAL_RATIOS: List[str] = [
    'Debt Cover = EBITDA / Interest Expense',
    'Size = ln(Total Assets)',
    'ROA = Profit After Tax / Total Assets',
    'Quick Ratio = (Total Current Assets - Inventory) / Total Current Liabilities',
    'Liabilities over Total Assets = Total Liabilities / Total Assets',
    'ROE = Profit After Tax / Total Equity',
    'Leverage = (Total Debt - Cash) / EBITDA',
    'Current Ratio = Total Current Assets / Total Current Liabilities',
]


def random_companies(number_of_companies: int, from_year: int, to_year: int):
    companies = []
    path = Path(NOUN_LIST_FILENAME)

    if path.is_file():
        print(f'Using file {path}')
        with path.open('r') as file:
            nouns = file.read().splitlines()
    else:
        print(f'Downloading noun list from {NOUN_LIST_URL} and saving to file {path}')
        with urllib.request.urlopen(NOUN_LIST_URL) as response, path.open('x') as file:
            decode = response.read().decode()
            file.write(decode)
            nouns = decode.splitlines()

    print(f'Using {len(nouns)} nouns to create {number_of_companies} companies:')
    for i in range(number_of_companies):
        company, created = create_company(
            name=f'{choice(nouns)} {choice(nouns)} {choice(nouns)}',
        )
        if created:
            companies.append(company)
            random_credit_reports(company=company, from_year=from_year, to_year=to_year, )
    print(f'{len(companies)} companies created, {number_of_companies - len(companies)} duplicates')


def random_credit_reports(company: Company, from_year: int, to_year: int):
    financial_reports: List[FinancialReport] = []
    for year in range(from_year, to_year + 1):
        date_time = datetime(year=year, month=randint(1, 12), day=randint(1, 28), tzinfo=timezone.utc)
        financial_report = create_financial_report(company=company, date_time=date_time, )
        random_financial_data(financial_report=financial_report)
        random_financial_ratio(financial_report=financial_report)
        financial_reports.append(financial_report)
        create_credit_report(
            company=company,
            probability_of_default=uniform(0, 1),
            credit_rating=choice(RATINGS),
            date_time=date_time,
            financial_reports=financial_reports,
        )


def random_financial_data(financial_report: FinancialReport):
    for name in FINANCIAL_DATA:
        create_financial_data(financial_report=financial_report, name=name, value=uniform(0, 999_999_999_999))


def random_financial_ratio(financial_report):
    for name in FINANCIAL_RATIOS:
        create_financial_ratio(financial_report=financial_report, name=name, value=uniform(-999_999, 999_999))
