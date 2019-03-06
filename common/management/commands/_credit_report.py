from datetime import datetime, timezone
from random import randint, choice, uniform
from typing import List

from company.models import Company
from credit_report.models import CreditReport

RATINGS: List[str] = [
    'AAA',
    'AA+',
    'AA',
    'AA-',
    'A+',
    'A',
    'A-',
    'BBB+',
    'BBB',
    'BBB-',
    'BB+',
    'BB',
    'BB-',
    'B+',
    'B',
    'B-',
    'CCC+',
    'CCC',
    'CCC-',
    'CC',
    'C',
    'D',
]


def create_credit_report(
        company: Company,
        probability_of_default: float,
        credit_rating: str,
        date_time: datetime,
) -> CreditReport:
    credit_report = CreditReport.objects.create(
        company_id=company.company_id,
        probability_of_default=probability_of_default,
        credit_rating=credit_rating,
        date_time=date_time,
    )
    print(f'        + Credit Report \'{credit_report.id}\' ({credit_report.date_time}) created', )
    return credit_report


def random_credit_report(company: Company, date_time: datetime, ) -> CreditReport:
    credit_report = create_credit_report(
        company=company,
        probability_of_default=uniform(0, 1),
        credit_rating=choice(RATINGS),
        date_time=date_time,
    )
    return credit_report


def random_credit_reports(company: Company, from_year: int, to_year: int) -> List[CreditReport]:
    credit_reports: List[CreditReport] = []
    for year in range(from_year, to_year + 1):
        date_time = datetime(year=year, month=randint(1, 12), day=randint(1, 28), tzinfo=timezone.utc, )
        credit_report = random_credit_report(company=company, date_time=date_time, )
        credit_reports.append(credit_report, )
    return credit_reports
