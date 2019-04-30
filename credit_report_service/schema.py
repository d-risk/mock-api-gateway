from graphene import Schema, ObjectType

from credit_report_service.company.schema import CompanyQuery
from credit_report_service.credit_rating.schema import CreditRatingQuery
from credit_report.schema import CreditReportQuery, CreditReportMutation
from credit_report_service.financial_report.schema import FinancialReportQuery
from credit_report_service.news.schema import NewsQuery


class Query(CompanyQuery, CreditReportQuery, FinancialReportQuery, NewsQuery, CreditRatingQuery, ObjectType):
    pass


class Mutation(CreditReportMutation, ObjectType):
    pass


schema: Schema = Schema(query=Query, mutation=Mutation)
