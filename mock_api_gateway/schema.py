from graphene import Schema, ObjectType

from mock_api_gateway.company.schema import CompanyQuery
from mock_api_gateway.credit_rating.schema import CreditRatingQuery
from mock_api_gateway.credit_report.schema import CreditReportQuery, CreditReportMutation
from mock_api_gateway.financial_report.schema import FinancialReportQuery
from mock_api_gateway.news.schema import NewsQuery


class Query(CompanyQuery, CreditReportQuery, FinancialReportQuery, NewsQuery, CreditRatingQuery, ObjectType):
    pass


class Mutation(CreditReportMutation, ObjectType):
    pass


schema: Schema = Schema(query=Query, mutation=Mutation)
