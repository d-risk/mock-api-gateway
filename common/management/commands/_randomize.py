import urllib.request
from pathlib import Path
from typing import List

from common.management.commands._company import random_companies
from common.management.commands._credit_report import random_credit_reports
from common.management.commands._financial_report import random_financial_reports
from common.management.commands._news import random_news_list
from company.models import Company

NOUN_LIST_URL = 'http://www.desiquintans.com/downloads/nounlist/nounlist.txt'
NOUN_LIST_FILENAME = 'noun_list.txt'


def nouns_list() -> List[str]:
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
    return nouns


def create_companies(number_of_companies: int, from_year: int, to_year: int, ):
    nouns: List[str] = nouns_list()
    print(f'Using {len(nouns)} nouns to create {number_of_companies} companies:')
    companies: List[Company] = random_companies(nouns=nouns, number_of_companies=number_of_companies)
    for company in companies:
        print(f'Company \'{company.name}\' ({company.company_id}):')
        random_credit_reports(company=company, from_year=from_year, to_year=to_year)
        random_financial_reports(company=company, from_year=from_year, to_year=to_year)
        random_news_list(nouns=nouns, company=company, from_year=from_year, to_year=to_year)
