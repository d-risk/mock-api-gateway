from datetime import datetime, timezone
from random import randint, choice, uniform
from typing import List

from mock_api_gateway.company.models import Company
from mock_api_gateway.risk_rating.models import RiskRating
from mock_api_gateway.risk_report.models import RiskReport


def create_risk_report(
        company: Company,
        risk_score: float,
        risk_rating: str,
        date_time: datetime,
) -> RiskReport:
    risk_report = RiskReport.objects.create(
        company_id=company.company_id,
        risk_score=risk_score,
        risk_rating=risk_rating,
        date_time=date_time,
    )
    print(f"        + Risk Report '{risk_report.report_id}' ({risk_report.date_time}) created", )
    return risk_report


def random_risk_report(company: Company, date_time: datetime, ) -> RiskReport:
    risk_report = create_risk_report(
        company=company,
        risk_score=uniform(RiskRating.AAA.value, RiskRating.D.value),
        risk_rating=choice(RiskRating.as_list()).readable_name,
        date_time=date_time,
    )
    return risk_report


def random_risk_reports(company: Company, from_year: int, to_year: int) -> List[RiskReport]:
    risk_reports: List[RiskReport] = []
    for year in range(from_year, to_year + 1):
        date_time = datetime(year=year, month=randint(1, 12), day=randint(1, 28), tzinfo=timezone.utc, )
        risk_report = random_risk_report(company=company, date_time=date_time, )
        risk_reports.append(risk_report, )
    return risk_reports
