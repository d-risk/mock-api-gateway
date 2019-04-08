from graphene import Schema, ObjectType

from company.schema import CompanyQuery
from credit_rating.schema import CreditRatingQuery
from credit_report.schema import CreditReportQuery, CreditReportMutation
from financial_report.schema import FinancialReportQuery
from news.schema import NewsQuery


class Query(CompanyQuery, CreditReportQuery, FinancialReportQuery, NewsQuery, CreditRatingQuery, ObjectType):
    pass


class Mutation(CreditReportMutation, ObjectType):
    pass


schema: Schema = Schema(query=Query, mutation=Mutation)
