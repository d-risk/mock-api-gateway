import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from random import randint, choice, uniform
from typing import List

from django_countries import countries

from common.management.commands._company import create_company
from common.management.commands._credit_report import create_credit_report
from common.management.commands._financial_report import create_financial_report, create_financial_data, \
    create_financial_ratio
from common.management.commands._news import create_news
from company.models import Company
from financial_report.models import FinancialReport
from news.models import News

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
            description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis posuere massa et ligula '
                        'semper, sed efficitur felis tincidunt. Etiam pellentesque dui vel feugiat porta. Nullam '
                        'mauris urna, dictum quis neque vel, rhoncus cursus tortor. Mauris at dignissim metus. Nam '
                        'ac eros sed turpis cursus tristique. Nam auctor commodo justo, sed volutpat risus '
                        'elementum quis. Orci varius natoque penatibus et magnis dis parturient montes, '
                        'nascetur ridiculus mus. Pellentesque lacinia nulla non erat blandit ultrices. Aenean '
                        'pharetra a eros vel varius. Quisque vitae ipsum sed neque tempor maximus. Vestibulum quis '
                        'leo fringilla, cursus tortor ac, finibus arcu.'
                        ''
                        'Cras ex velit, lobortis quis malesuada quis, dignissim vitae eros. Praesent arcu nibh, '
                        'porttitor eget dui sed, convallis venenatis justo. Donec a quam non velit fermentum '
                        'suscipit. Duis ultrices iaculis mauris, at malesuada odio feugiat ac. Nullam et accumsan '
                        'nibh. Proin libero magna, tempus sit amet tincidunt sit amet, venenatis eget dui. Cras '
                        'dignissim, felis et consectetur bibendum, tellus elit dignissim velit, sed faucibus enim '
                        'ipsum eget lectus. Vestibulum lobortis rhoncus nulla. Vestibulum hendrerit lorem orci, '
                        'id hendrerit lorem accumsan vel. Nunc elementum tortor quam, id lacinia turpis aliquam a. '
                        'Sed vel vestibulum augue. Donec vulputate et justo vel tincidunt.',
            industry=choice(nouns),
            exchange=f'stock {choice(nouns)} exchange',
            country=choice(countries)
        )
        if created:
            companies.append(company, )
            random_credit_reports(nouns=nouns, company=company, from_year=from_year, to_year=to_year, )
    print(f'{len(companies)} companies created, {number_of_companies - len(companies)} duplicates')


def random_credit_reports(nouns, company: Company, from_year: int, to_year: int):
    financial_reports: List[FinancialReport] = []
    news: List[News] = []
    for year in range(from_year, to_year + 1):
        date_time = datetime(year=year, month=randint(1, 12), day=randint(1, 28), tzinfo=timezone.utc, )
        financial_report = create_financial_report(company=company, date_time=date_time, )
        random_financial_data(financial_report=financial_report, )
        random_financial_ratio(financial_report=financial_report, )
        financial_reports.append(financial_report, )
        n = create_news(
            company=company,
            title=choice(nouns),
            date_time=date_time,
            snippet='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis posuere massa et ligula '
                    'semper, sed efficitur felis tincidunt. Etiam pellentesque dui vel feugiat porta. Nullam '
                    'mauris urna, dictum quis neque vel, rhoncus cursus tortor. Mauris at dignissim metus. Nam '
                    'ac eros sed turpis cursus tristique. Nam auctor commodo justo, sed volutpat risus '
                    'elementum quis. Orci varius natoque penatibus et magnis dis parturient montes, '
                    'nascetur ridiculus mus. Pellentesque lacinia nulla non erat blandit ultrices. Aenean '
                    'pharetra a eros vel varius. Quisque vitae ipsum sed neque tempor maximus. Vestibulum quis '
                    'leo fringilla, cursus tortor ac, finibus arcu.',
            url=f'https://example.com/{choice(nouns)}-{choice(nouns)}-{choice(nouns)}-{choice(nouns)}'
        )
        news.append(n, )
        create_credit_report(
            company=company,
            probability_of_default=uniform(0, 1),
            credit_rating=choice(RATINGS),
            date_time=date_time,
            financial_reports=financial_reports,
            news=news,
        )


def random_financial_data(financial_report: FinancialReport):
    for name in FINANCIAL_DATA:
        create_financial_data(financial_report=financial_report, name=name, value=uniform(0, 999_999_999_999))


def random_financial_ratio(financial_report):
    for name in FINANCIAL_RATIOS:
        create_financial_ratio(financial_report=financial_report, name=name, value=uniform(-999_999, 999_999))


