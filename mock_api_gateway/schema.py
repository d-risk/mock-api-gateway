from graphene import Schema, ObjectType

from mock_api_gateway.company.schema import CompanyQuery
from mock_api_gateway.risk_rating.schema import RiskRatingQuery
from mock_api_gateway.risk_report.schema import RiskReportQuery, RiskReportMutation
from mock_api_gateway.financial_report.schema import FinancialReportQuery
from mock_api_gateway.news.schema import NewsQuery


class Query(CompanyQuery, RiskReportQuery, FinancialReportQuery, NewsQuery, RiskRatingQuery, ObjectType):
    pass


class Mutation(RiskReportMutation, ObjectType):
    pass


schema: Schema = Schema(query=Query, mutation=Mutation)
